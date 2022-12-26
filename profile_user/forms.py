# Django
from django import forms
from django.core.validators import validate_image_file_extension
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# Model
from profile_user.models import User, ProfileUser


class CustomPhoneNumberPrefixWidget(PhoneNumberPrefixWidget):
   
    def subwidgets(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        return context['widget']['subwidgets']


class SignupFormUser(forms.Form):
    """Sign up form."""

    DOCUMENT_TYPE_CHOICES = [
        ('CC', 'CEDULA DE CIUDADANIA'),
        ('CE', 'CEDULA DE EXTRANJERIA'),
        ('PA', 'PASAPORTE'),
        ('TI', 'TARJETA DE IDENTIDAD'),
        ('IT', 'IDENTIFICACION TRIBUTARIA'),
        ('IP', 'IDENTIFICACION PERSONAL'),
    ] 

    TYPE_CHARGE_CHOICES = [
        ('administrator', 'administrator'),
        ('assistant', 'assistant'),
        ('masseur', 'masseur'),
    ]

    first_name = forms.CharField(min_length=2, max_length=50, widget=forms.TextInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-800 focus:border-indigo-800 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-800 dark:focus:border-indigo-800'}))
    last_name = forms.CharField(min_length=2, max_length=50, widget=forms.TextInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}))
    username = forms.CharField(min_length=4, max_length=50, widget=forms.TextInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}))
    password = forms.CharField(max_length=70, widget=forms.PasswordInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}))
    password_confirmation = forms.CharField(max_length=70, widget=forms.PasswordInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}))
    document_type = forms.ChoiceField(choices=DOCUMENT_TYPE_CHOICES, widget=forms.Select(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}))
    document_number = forms.IntegerField(min_value=4, widget=forms.NumberInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}))
    email = forms.CharField(min_length=6, max_length=70, widget=forms.EmailInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}))
    address = forms.CharField(min_length=4, max_length=50, widget=forms.TextInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}))
    academy = forms.CharField(min_length=4, max_length=50, widget=forms.TextInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}))
    expiration_date_biosafety = forms.DateField(widget=forms.DateTimeInput(format=('%Y-%m-%d'), attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white', 'type': 'date'}))
    position = forms.ChoiceField(choices=TYPE_CHARGE_CHOICES, widget=forms.Select(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}))
    phone_number = PhoneNumberField(widget=CustomPhoneNumberPrefixWidget(initial='CO', attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}))
    picture = forms.ImageField(widget=forms.FileInput(attrs = {"id" : "image_field",'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'}),required=False, validators=[validate_image_file_extension])

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use.')
        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError({'password': forms.ValidationError('Passwords do not match.')})
        return data

    def clean_email(self):
        """Email must be unique."""
        email = self.cleaned_data['email']
        email_taken = User.objects.filter(email=email).exists()
        if email_taken:
            raise forms.ValidationError('Email is already in use.')
        return email   

    def clean_document_number(self):
        """Document_number must be unique."""
        document_number = self.cleaned_data['document_number']
        document_number_taken = ProfileUser.objects.filter(document_number=document_number).exists()
        if document_number_taken:
            raise forms.ValidationError('Document number is already in use.')
        return document_number   

    def clean_phone_number(self):
        """phone_number must be unique."""
        phone_number = self.cleaned_data['phone_number']
        phone_number_taken = ProfileUser.objects.filter(phone_number=phone_number).exists()
        if phone_number_taken:
            raise forms.ValidationError('Phone number is already in use.')
        return phone_number   

    def save(self):
        """Create user and profile."""
        data = self.cleaned_data
        data.pop('password_confirmation')
        
        username = data['username'] 
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        document_type = data['document_type']
        document_number = data['document_number']
        address = data['address']
        phone_number = data['phone_number']
        academy = data['academy']
        expiration_date_biosafety = data['expiration_date_biosafety']
        picture = data['picture']
        position = data['position']

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        ProfileUser.objects.create(user=user, document_type=document_type, document_number=document_number, 
                                    picture=picture, phone_number=phone_number, 
                                    address=address, academy=academy,
                                    expiration_date_biosafety=expiration_date_biosafety,
                                    position=position)


class UpdateFormUser(forms.ModelForm):
    """ form model update profile. """
    
    class Meta:

        model = ProfileUser
        fields = ('document_type', 'document_number', 'phone_number', 'address', 'academy', 'expiration_date_biosafety', 'position')
        widgets = {
            
            'document_type' : forms.Select(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'document_number' : forms.NumberInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'address' : forms.TextInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'academy' : forms.TextInput(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'expiration_date_biosafety' : forms.DateTimeInput(format=('%Y-%m-%d'), attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white', 'type': 'date'}),
            'position' : forms.Select(attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
            'phone_number' : CustomPhoneNumberPrefixWidget(initial='CO', attrs={'class':'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-600 focus:border-indigo-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-indigo-600 dark:focus:border-indigo-600'}),
        }