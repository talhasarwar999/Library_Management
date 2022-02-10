from django import forms
from library.models import Book
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['bookname','authorname','isbn','nofpages','category','description','image']