from .models import BookModel, ReviewModel
from .forms import ContactForm, ReviewForm


def menu(request):
    recommended_books = BookModel.objects.all()[0:4]
    search = BookModel.objects.all()
    review_show = ReviewModel.objects.all().order_by('-posted')[0:4]
    form = ContactForm()
    review = ReviewForm()

    if request.method == 'POST':
        if form.is_valid():
            form.save()

    return {'recommended': recommended_books,
            'search': search,
            'form': form,
            'review': review,
            'review_show': review_show}
