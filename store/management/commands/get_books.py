from  datetime import datetime
from urllib.parse import urlparse
from django.db.utils import IntegrityError
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import *
from requests_html import HTMLSession
from django.core.files.base import ContentFile
import requests
import logging

logger = logging.getLogger('django_log')

locker = Lock()


def crawler(url):

    with HTMLSession() as session:
        response = session.get(url)

    name = response.html.xpath('//h1')[0].text
    price = response.html.xpath('//div[@class="abaproduct-price"]')[0].text
    publisher = response.html.xpath('//fieldset[@id="aba-product-details-fieldset"]/text()[7]')[0]
    try:
        description = response.html.xpath('//div[@class="abaproduct-body"]')[0].text
    except IndexError:
        logger.error(f'Error while parsing description{IndexError}')
        description = 'No description'
    isbn = response.html.xpath('//fieldset[@id="aba-product-details-fieldset"]/text()[3]')[0]
    pages = response.html.xpath('//fieldset[@id="aba-product-details-fieldset"]/text()[11]')[0]
    # pub_date = response.html.xpath('//fieldset[@id="aba-product-details-fieldset"]/text()[9]')[0]
    img_source = response.html.xpath('//div[@class="abaproduct-large-image"]/a/img/@src')
    # related_edition = response.html.xpath('//fieldset[@class="collapsible abaproduct-related-editions"][2]/ul/li/a') #loop
    author = response.html.xpath('//div[@class="abaproduct-authors"]/a')[0].text
    try:
        about_author = response.html.xpath('//div[@class="abaproduct-body"][2]')[0].text
    except IndexError:
        logger.error(f'Error while parsing about_author{IndexError}')
        about_author = 'No info about author'
    category = response.html.xpath('//fieldset[@class="collapsible abaproduct-related-editions"][1]/ul/li/a')  #loop

    try:
        with locker:
            athr = BookAuthor.objects.create(author_name=author, about_author=about_author)
    except IntegrityError:
        logger.error(f'Error while creating book author{IntegrityError}')
        print('db was locker while author creating')
        return

    book = {
        'name': name,
        'price': price,
        'publisher': publisher,
        'description': description,
        'isbn': isbn,
        'pages': pages,
        'author': athr,
        'img_source': img_source,
    }

    try:
        with locker:
            bm = BookModel.objects.create(**book)
    except Exception as e:
        logger.error(e)
        print('db was locker while book creating')
        print(type(e), e)
        return

    for cat in category:
        cat = {'name': cat.text, 'slug': slugify(cat)}
        try:
            with locker:
                cat, created = BookCategory.objects.get_or_create(**cat)
            bm.category.add(cat)
        except Exception as e:
            print('db was locker while cat creating')
            print(type(e), e)
            return

    name = urlparse(img_source[0]).path.split('/')[-1]
    resp = requests.get(img_source[0])
    bm.cover.save(name, ContentFile(resp.content), save=True)
    bm.save()


isbn = []


def isbn_creater():
    book_url = 'https://www.boulderbookstore.net/browse/book?page='
    url = 'https://www.boulderbookstore.net/book/'
    # url2 = 'https://www.boulderbookstore.net/book/9781982121082'
    # Thread(target=crawler, args=(url2, )).start()

    try:
        with HTMLSession() as session:
            for t in range(1, 20):
                response = session.get(book_url + str(t))
                book_img = response.html.xpath('//div[@class="abaproduct-image"]/a/img/@src')
                print('done')
                for i in book_img:
                    isbn.append(i.split('/')[7][2:15])
    except ConnectionError:
        print('parse failed')


def urls_generator(task):
    isbn_creater()
    for i in isbn:
        url = f'https://www.boulderbookstore.net/book/{i}'
        logger.info(f'url was created - {url}')
        with locker:
            task.status = f'scrape id: {i}'
            task.save()
        yield url


def run_crawler(task):
    task.status = 'start parsing'
    task.save()
    url_gen = urls_generator(task)
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(crawler, url_gen)
    task.status = 'finished'
    task.end_time = datetime.now()
    task.save()


class Command(BaseCommand):
    help = 'Book scraper'

    def handle(self, *args, **options):
        from tasks.models import Task

        task = Task.objects.create(name='run_scraper')
        run_crawler(task)
