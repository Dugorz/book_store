from django.test import TestCase, RequestFactory
from .models import BookModel, BookAuthor, BookCategory, ContactModel, ReviewModel
import datetime
from .views import IndexView


class BaseModelTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        super(BaseModelTestCase, cls).setUpClass()
        cls.author = BookAuthor(author_name='George', about_author='Pedestrian', slug='George')
        cls.author.save()
        cls.category = BookCategory(name='Action', slug='action')
        cls.category.save()
        cls.book = BookModel(name='Harry Potter', price=4.55, publisher='John Kennedy', description='Book about books',
                             isbn=9379992, rate=5, pages=25, added=datetime.datetime.now().date(), cover=None,
                             available=True, slug='HarryPotter', author=cls.author, img_source=None, book_source=None)
        cls.book.save()
        cls.book.category.add(cls.category)
        cls.book.save()
        cls.review = ReviewModel(name='Frank', review='Nice book', book=cls.book, posted=datetime.datetime.now())
        cls.review.save()
        cls.contact = ContactModel(name='Frank', email='frank@mail.com', message='Noice site',
                                   sent=datetime.datetime.now().date())
        cls.contact.save()

    def view_test(self):
        request = self.factory.get('/')
        home_obj = IndexView()
        home_obj.request = request
        result_context = home_obj.get_context_data()
        self.assertTrue('1984 (Paperback)' in result_context)


class BookModelTestCase(BaseModelTestCase):
    def test_created_properly(self):
        self.assertEqual(self.book.name, 'Harry Potter')
        self.assertEqual(self.book.price, 4.55)
        self.assertEqual(self.book.publisher, 'John Kennedy')
        self.assertEqual(self.book.description, 'Book about books')
        self.assertEqual(self.book.isbn, 9379992)
        self.assertEqual(self.book.rate, 5)
        self.assertEqual(self.book.pages, 25)
        self.assertEqual(self.book.added, self.book.added)
        self.assertEqual(self.book.cover, None)
        self.assertEqual(self.book.available, True)
        self.assertEqual(self.book.slug, 'HarryPotter')
        self.assertEqual(self.book.author, self.book.author)
        self.assertEqual(self.book.category, self.book.category)
        self.assertEqual(self.book.img_source, None)
        self.assertEqual(self.book.book_source, None)

    def test_str(self):
        self.assertEqual(self.book.__str__(), 'Harry Potter')

    def get_absolute_str_test(self):
        self.assertEqual(self.book.get_absolute_url(), 'harry')


class BookAuthorTestCase(BaseModelTestCase):
    def test_created_properly(self):
        self.assertEqual(self.author.author_name, 'George')
        self.assertEqual(self.author.about_author, 'Pedestrian')
        self.assertEqual(self.author.slug, 'George')

    def test_str(self):
        self.assertEqual(self.author.__str__(), 'George')

    def get_absolute_str_test(self):
        self.assertEqual(self.author.get_absolute_url(), 'George')


class BookCategoryTestCase(BaseModelTestCase):
    def test_created_properly(self):
        self.assertEqual(self.category.name, 'Action')
        self.assertEqual(self.category.slug, 'action')

    def test_str(self):
        self.assertEqual(self.category.__str__(), 'Action')

    def get_absolute_str_test(self):
        self.assertEqual(self.category.get_absolute_url(), 'action')


class ContactTestCase(BaseModelTestCase):
    def test_created_properly(self):
        self.assertEqual(self.contact.name, 'Frank')
        self.assertEqual(self.contact.email, 'frank@mail.com')
        self.assertEqual(self.contact.message, 'Noice site')
        self.assertEqual(self.contact.sent, self.contact.sent)

    def test_str(self):
        self.assertEqual(self.contact.__str__(), 'Frank')
