
from django import forms
from .models import Product
import re
class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Add custom validation logic here
        if not username:
            self.add_error('username', 'Username is required.')
        if not password:
            self.add_error('password', 'Password is required.')

        return cleaned_data

def contains_special_characters(value):
    # Regular expression to match special characters
    special_characters_regex = re.compile(r'[!@#$%^&*(),.?":{}|<>]')
    # Check if the input value contains any special characters
    if special_characters_regex.search(value):
        raise forms.ValidationError("Input contains special characters.")
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'image'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        image = cleaned_data.get("image")

        # Add custom validation logic here
        if not name:
            self.add_error('name', 'Name is required.')
        if not image:
            self.add_error('image', 'Image is required.')

        return cleaned_data
        
     #Input Validation   
    def clean_name(self):
        data = self.cleaned_data['name']
        characters_to_check = "'!@#$%^&*()'/" + '""'
        if contains_specific_characters(data, characters_to_check):
            raise forms.ValidationError("Input cannot contain special characters.")
        return data

def contains_specific_characters(input_string, characters):
    pattern = re.compile(r'[' + re.escape(characters) + ']')
    if pattern.search(input_string):
        return True
    else:
        return False