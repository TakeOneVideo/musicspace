from django import forms
from musicspace_app.models import Address, Provider, MusicspaceUser, Genre, Instrument

class MusicspaceUserForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = MusicspaceUser
        fields = [
            'first_name', 'last_name'
        ]

class AddressForm(forms.ModelForm):
    
    street_1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    street_2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Address
        fields = [
            'street_1', 'street_2', 'city',
            'state', 'zip'
        ]

class ProviderForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    image_url = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    instruments = forms.ModelMultipleChoiceField(
        queryset=Instrument.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    
    in_person = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    online = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Provider
        fields = [
            'title', 'text', 'image_url', 
            'genres', 'instruments',
            'in_person', 'online'
        ]