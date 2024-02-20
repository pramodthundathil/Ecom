from django.forms import ModelForm,TextInput,Select
from .models import ProductDetails

class ProductAddForm(ModelForm):
    class Meta:
        model = ProductDetails
        fields = ["product_name","Product_category","Product_subcategory","product_description","product_price","product_stock","Product_Image"]
        
        widgets = {
            "product_name":TextInput(attrs={"class":'form-control'}),
            "Product_category":Select(attrs={"class":'form-control'}),
            "Product_subcategory":Select(attrs={"class":'form-control'}),
            "product_description":TextInput(attrs={"class":'form-control'}),
            "product_price":TextInput(attrs={"type":"number","class":'form-control'}),
            "product_stock":TextInput(attrs={"type":"number","class":'form-control'}),
            
        }
