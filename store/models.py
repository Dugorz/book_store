from django.db import models
from django.urls import reverse


class BookModel(models.Model):
    name = models.CharField(max_length=200, verbose_name='Book name')
    price = models.CharField(max_length=200, verbose_name='Book price')
    publisher = models.CharField(max_length=100, verbose_name='Book publisher')

    description = models.TextField()

    isbn = models.BigIntegerField(verbose_name='Book ISBN')
    rate = models.IntegerField(verbose_name='Book rating', default=0)
    pages = models.IntegerField(verbose_name='Pages')

    # pub_date = models.DateField(verbose_name='Publish date')
    added = models.DateTimeField(auto_now_add=True, verbose_name='Book added')

    cover = models.ImageField(verbose_name='Book cover', upload_to='media/%Y%m%d%h/cover', blank=True, null=True,
                              default=None)
    available = models.BooleanField(verbose_name='Book available', default=True)
    slug = models.SlugField(unique=True, verbose_name='Book Slug', max_length=150)

    author = models.ForeignKey('BookAuthor', verbose_name='Book author', related_name='authors',
                               on_delete=models.CASCADE)
    # related_edition = models.ForeignKey('self', verbose_name='Related books', related_name='related_books',
    #                                     on_delete=models.DO_NOTHING)
    category = models.ManyToManyField('BookCategory', verbose_name='book category', related_name='category')

    img_source = models.URLField(max_length=255, blank=True, null=True)
    book_source = models.URLField(max_length=255, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     self.slug = self.name.replace(' ', '')[0:10]
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class BookAuthor(models.Model):
    author_name = models.CharField(max_length=200, verbose_name='Book author_name')
    about_author = models.TextField()
    slug = models.SlugField(max_length=250, unique=True)

    def save(self, *args, **kwargs):
        self.slug = self.author_name.replace(' ', '')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('author_filter', kwargs={'slug': self.slug})

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = 'Book author_name'
        verbose_name_plural = 'Books authors'


class BookCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='Book category')
    slug = models.SlugField(unique=True, max_length=150)

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.name})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ContactModel(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Message')
    sent = models.DateTimeField(auto_now_add=True, verbose_name='Sent')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact request'
        verbose_name_plural = 'Contact requests'


class ReviewModel(models.Model):
    name = models.CharField(max_length=200, verbose_name='Author name')
    review = models.TextField(verbose_name='Book review')
    book = models.ForeignKey(BookModel, verbose_name='Book', related_name='book', on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True, verbose_name='Review added')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
