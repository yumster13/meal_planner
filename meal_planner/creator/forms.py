from django import forms
from database.models import *

DATE_INPUT_FORMATS = ['%Y-%m-%d']
class DateInput(forms.DateInput):
    input_type = 'date'
    input_formats = DATE_INPUT_FORMATS


class SearchDate(forms.Form):
    date = forms.DateField(widget=DateInput())

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = []

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['road', 'town', 'number', 'codePostal', 'country']

class CampForm(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ['name','section','deadline', 'from_date','to_date','type']
        widgets = {
            'deadline': DateInput(),
            'from_date': DateInput(),
            'to_date': DateInput(),
        }

class CreateUser(forms.Form):
    email = forms.EmailField()
    section = forms.ModelChoiceField(queryset=Section.objects.all())

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['nbr_anim','nbr_leaders','nbr_vege','date','moment','recipe']
        widgets = {
            'date': DateInput(),
        }

class MenuFormNoDate(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['nbr_anim','nbr_leaders','nbr_vege','moment','recipe']

class CampFormUpdate(forms.ModelForm):
    location = AddressForm()
    class Meta:
        model = Camp
        fields = ['from_date','to_date','deadline','section']
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput(),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if from_date and to_date:
            if from_date >= to_date:
                raise forms.ValidationError("The 'from_date' must be before the 'to_date'.")

        return cleaned_data
    
