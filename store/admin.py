from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


class BookAdmin(SummernoteModelAdmin):
    fields = ('name', 'description', 'cover', 'price', 'available', 'slug')
    list_display = ('name', 'price', 'added', 'available')
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}
    summernote_fields = ('description',)


class BookAuthorAdmin(admin.ModelAdmin):
    fields = ('author_name', 'about_author', 'slug')
    list_display = ('author_name', )
    prepopulated_fields = {'slug': ('author_name', )}
    search_fields = ('author_name', )


class BookCategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'slug')
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name', )}
    search_fields = ('name', )


class ContactAdmin(admin.ModelAdmin):
    fields = ('name', 'email', 'message')
    list_display = ('name', 'sent')
    list_filter = ('sent', )


class ReviewAdmin(admin.ModelAdmin):
    fields = ('name', 'review', 'book')
    list_display = ('name', 'posted')
    list_filter = ('name', 'posted')


admin.site.register(BookModel, BookAdmin)
admin.site.register(ReviewModel, ReviewAdmin)
admin.site.register(ContactModel, ContactAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookCategory, BookCategoryAdmin)
