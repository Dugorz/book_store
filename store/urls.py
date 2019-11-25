from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', IndexView.as_view(), name='index_view'),
    path('shop', cache_page(60 * 5)(ShopView.as_view()), name='shop_view'),
    path('book/<str:slug>', BookDetailView.as_view(), name='book_detail'),
    path('about', AboutView.as_view(), name='about_url'),
    path('faq', FaqView.as_view(), name='faq_url'),
    path('search/', SearchView.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
