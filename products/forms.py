from django import forms

from .models import Product

FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "price", "image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной")
        return price

    def clean_name(self):
        name = self.cleaned_data['name']
        name_lower = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(f"Слово '{word}' запрещено использовать в названии")
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        description_lower = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in description_lower:
                raise forms.ValidationError(f"Слово '{word}' запрещено использовать в описании")
        return description