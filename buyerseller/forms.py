from .models import *
from django import forms
from django.utils.translation import gettext_lazy as _


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ordered_by", "shipping_address",
                  "mobile", "email", "payment_method"]


class ProdCommentForm(forms.ModelForm):
    class Meta:
        model = ProdComment
        fields = ('name', 'email', 'mobile', 'body')


class ProdInquiryForm(forms.ModelForm):
    class Meta:
        model = ProdComment
        fields = ('body','name', 'email', 'mobile')


class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))

    class Meta:
        model = Product
        fields = ["title", "slug", "keyfeatures", "category", "image",
                  "description", "warranty", "return_policy",
                  "brand", "uom", "marked_price", "selling_price", "offer","noofpacksinonecartoon", "moq", "storagetemp", "show_product", "policy_agreed"]
        labels = {
            'policy_agreed': _('By clicking submit, you acknowledge that your information does not violate any listing policies.'),
            'show_product': _(' Display this product on showcase'),
            'category': _('Click to select product Category'),
            'title': _('Product Name - English'),
            'keyfeatures': _('Key features - English'),
            'slug': _('Keywords/Slug -English'),
            'marked_price': _('Please enter Unit  price'),
            'selling_price': _('Please enter Sale price'),
            'uom': _('Price unit of measure'),
            'warranty': _('Please enter product warrant policy'),
            'return_policy': _('Please enter return policy '),
            'brand': _('Product Brand Name'),
            'noofpacksinonecartoon': _('Number Of Packs in one cartoon'),
            'storagetemp': _('Minimum Storage Temperature required for this product'),
            'moq': _('Minimum order quantity'),
            'description': _(
                'Long Product Description. You may include: color, size, material, grade/standard, etc. Max.40000 Character Limit.')
        }
        widgets = {
            "keyfeatures": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Eg. Apple Product, 5TB, 6GB Memory, 2 year warranty"
            }),
            "brand": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product brand here..."
            }),
            "storagetemp": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the storage temperature required for product here..."
            }),

            "uom": forms.Select(attrs={
                "class": "form-control"
            }),
            "noofpacksinonecartoon": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "No. of packs in one cartoon. here...."
            }),
            "moq": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Minimum Order Quantity here..."
            }),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Macbook Pro 2020"
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the unique slug / keyword eg.Laptop "
            }),
            "category": forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Click to select category"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "marked_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Marked price of the product..."
            }),
            "selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Selling price of the product..."
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of the product...",
                "rows": 5
            }),
            "warranty": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product warranty here..."
            }),
            "return_policy": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product return policy here..."
            }),

        }


class RfqForm(forms.ModelForm):
    more_images = forms.FileField(required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control",
                                                                "multiple": True
                                                                }))

    class Meta:
        model = Rfq

        fields = ['industry', 'buyer_need', 'keywords', 'content', 'qty_required', 'uom',
                  'buying_frequency', 'image', 'payment_mode', 'destination_port', 'time_validity','policy_agreed']
        labels = {
            'policy_agreed': _('I have read, agreed to abide by Terms and Conditions of RFQ'),
            'industry': _('Please select industry'),
            'buyer_need': _('Please enter title of Buy Offer'),
            'keywords': _('Please enter comma seperated keywords.Example: shoes,clothes,eyewear etc'),
            'qty_required': _('Please enter required quantity'),
            'uom': _('Please select proper unit'),
            'buying_frequency': _('Please enter buying frequency'),
            'image': _('Attachment like product pictures/images would improve your RFQ'),
            'payment_mode': _('Preffered Payment Methods:'),
            'time_validity': _('Select Time Of Validity'),
            'destination_port': _('Destination Port Name Details'),
            'content': _(
                'Please let suppliers know your detailed requirements. You may include: color, size, material, grade/standard, etc'),
            'more_images': _('Add more images to your product info'),
        }

        widgets = {
            "industry": forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Please Select Industry*"
            }),
            "buyer_need": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Tell us what you want to buy"
            }),
            "keywords": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Keywords..."
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Tell suppliers your requirements",
                "rows": 5
            }),
            "qty_required": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Quantity Required*"
            }),
            "uom": forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Select Unit*"
            }),
            "buying_frequency": forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Select Buying Frequeny"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "payment_mode": forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Mode of payments"
            }),
            "destination_port": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Destination Port"
            }),
            " time_validity": forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Select Time of Validity"
            }),
        }


class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())



