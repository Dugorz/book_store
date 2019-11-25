from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect

from .models import BookModel
from .forms import ReviewForm
import logging

logger = logging.getLogger('django_log')
shop_log = logging.getLogger('shop_log')


class IndexView(ListView):
    template_name = 'index.html'
    paginate_by = 30
    model = BookModel

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = BookModel.objects.all()

        logger.debug(context)
        return context


class ShopView(ListView):
    template_name = 'shop.html'
    model = BookModel
    paginate_by = 30


class AboutView(TemplateView):
    template_name = 'about.html'


class FaqView(TemplateView):
    template_name = 'faq.html'


class BookDetailView(FormMixin, DetailView):
    template_name = 'product-single.html'
    model = BookModel
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = BookModel.objects.all()
        context['rec_books'] = BookModel.objects.all().order_by('-rate')[0:4]
        context['review'] = ReviewForm(initial={'book': self.object})

        logger.debug(context)

        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        form = self.get_form()

        logger.debug(request)

        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()

            return HttpResponseRedirect(reverse('book_detail', kwargs={'slug': book.slug}))

        return reverse('book_detail', kwargs={'slug': book.slug})


class SearchView(ListView):
    template_name = 'shop.html'
    paginate_by = 30

    def get_queryset(self):
        query = self.request.GET.get('q')
        logger.debug(query)
        if query:
            return BookModel.objects.filter(name__contains=query)
        else:
            return BookModel.objects.all()
