from django import forms


# class ChoiceSize(forms.ModelForm):
#     class Meta:
#         model: Products
#         size = forms.TypedChoiceField


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label="", initial=1, min_value=1, widget=forms.NumberInput(attrs={"class":"size_list text_20 opacity100"}))
    #quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    #size = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
