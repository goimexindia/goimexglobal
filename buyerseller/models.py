from ckeditor.fields import RichTextField
from django_countries.fields import CountryField
from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from PIL import Image
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.urls import reverse_lazy, reverse
from mptt.models import MPTTModel, TreeForeignKey

UOM = [
    ("Case", "Case"),
    ("Centimeter", "Centimeter"),
    ("Chain", "Chain"),
    ("Cubic Centimeter", "Cubic Centimeter"),
    ("Cubic Foot", "Cubic Foot"),
    ("Cubic Inch", "Cubic Inch"),
    ("Cubic Meter", "Cubic Meter"),
    ("Cubic Yard", "Cubic Yard"),
    ("DEGREES Celsius", "DEGREES Celsius"),
    ("Degrees Fahrenheit", "Degrees Fahrenheit"),
    ("Dozen", "Dozen"),
    ("Dram", "Dram"),
    ("Fluid Ounce", "Fluid Ounce"),
    ("Foot", "Foot"),
    ("Forty-Foot Container ", "Forty-Foot Container"),
    ("Furlong", "Furlong"),
    ("Gallon", "Gallon"),
    ("Gill", "Gill"),
    ("Grain", "Grain"),
    ("Gram", "Gram"),
    ("Gross", "Gross"),
    ("Hectare", "Hectare"),
    ("Hertz", "Hertz"),
    ("Inch", "Inch"),
    ("Kiloampere", "Kiloampere"),
    ("Kilogram", "Kilogram"),
    ("Kilohertz", "Kilohertz"),
    ("Kilometer", "Kilometer"),
    ("Kiloohm", "Kiloohm"),
    ("Kilovolt", "Kilovolt"),
    ("Kilowatt", "Kilowatt"),
    ("Liter", "Liter"),
    ("Long Ton", "Long Ton"),
    ("Megahertz", "Megahertz"),
    ("Meter", "Meter"),
    ("Metric Ton", "Metric Ton"),
    ("Mile", "Mile"),
    ("Milliampere", "Milliampere"),
    ("Milligram", "Milligram"),
    ("Millihertz", "Millihertz"),
    ("Milliliter", "Milliliter"),
    ("Millimeter", "Millimeter"),
    ("Milliohm", "Milliohm"),
    ("Millivolt", "Millivolt"),
    ("Milliwatt", "Milliwatt"),
    ("Nautical Mile", "Nautical Mile"),
    ("Ohm", "Ohm"),
    ("Ounce", "Ounce"),
    ("Pack", "Pack"),
    ("Pallet", "Pallet"),
    ("Pair", "Pair"),
    ("Parcel", "Parcel"),
    ("Perch", "Perch"),
    ("Piece", "Piece"),
    ("Pint", "Pint"),
    ("Plant", "Plant"),
    ("Pole", "Pole"),
    ("Pound", "Pound"),
    ("Quart", "Quart"),
    ("Quarter", "Quarter"),
    ("Rod", "Rod"),
    ("Roll", "Roll"),
    ("Set", "Set"),
    ("Sheet", "Sheet"),
    ("Short Ton", "Short Ton"),
    ("Square Centimeter", "Square Centimeter"),
    ("Square Foot", "Square Foot"),
    ("Square Inch", "Square Inch"),
    ("Square Meter", "Square Meter"),
    ("Square Mile", "Square Mile"),
    ("Square Yard", "Square Yard"),
    ("Stone", "Stone"),
    ("Strand", "Strand"),
    ("Ton", "Ton"),
    ("Tonne", "Tonne"),
    ("Tray", "Tray"),
    ("Twenty-Foot Container", "Twenty-Foot Container"),
    ("Unit", "Unit"),
    ("Volt", "Volt"),
    ("Watt", "Watt"),
    ("Wp", "Wp"),
    ("Yard", "Yard"),
]

FREQUENCY = [
    ('1 week', '1 Week'),
    ('2 week', '2 Week'),
    ('3 week', '3 Week'),
    ('1 month', '1 Month'),
    ('2 month', '2 Month'),
    ('3 month', '3 Month'),
    ('4 month', '4 Month'),
    ('5 month', '5 Month'),
    ('6 month', '6 Month'),
    ('1 year', '1 Year'),
]

FREQUENCY1 = [
    ('one time', 'One time'),
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('semi annually', 'Semi Annually'),
    ('annually', 'Annually'),
    ('others', 'Others'),
]

PAYMENT = [
    ('t/t', 'T/T'),
    ('l/c', 'L/C'),
    ('d/a', 'D/A'),
    ('d/p', 'D/P'),
    ('western union', 'WESTERN UNION'),
    ('money gram', 'Money Gram'),
    ('paypal', 'PayPal'),
    ('others', 'OTHERS')
]
INDUSTRY = [
    ('AGRICULTURE', 'Agriculture'),
    ('APPAREL', 'Apparel'),
    ('AUTOMOBILES & MOTORCYCLES', 'Automobiles & Motorcycles'),
    ('BEAUTY & PERSONAL CARE', 'Beauty & Personal Care'),
    ('CHEMICALS', 'Chemicals'),
    ('COMPUTER HARDWARE & SOFTWARE', 'Computer Hardware & Software'),
    ('CONSTRUCTION & REAL ESTATE', 'Construction & Real Estate'),
    ('CONSUMER ELECTRONICS', 'Consumer Electronics'),
    ('ELECTRICAL EQUIPMENT SUPPLIES', 'Electrical Equipment Supplies'),
    ('ENERGY', 'Energy'),
    ('ENVIRONMENT', 'Environment'),
    ('FASHION ACCESSORIES', 'Fashion Accessories'),
    ('FOOD & BEVERAGE', 'Food & Beverage'),
    ('FURNITURE', 'Furniture'),
    ('GIFTS & CRAFTS', 'Gifts & Crafts'),
    ('HARDWARE', 'Hardware'),
    ('HEALTH & MEDICAL', 'Health & Medical'),
    ('HOME & GARDEN', 'Home & Garden'),
    ('HOME APPLIANCES', 'Home Appliances'),
    ('INDUSTRIAL PARTS & FABRICATION SERVICES', 'Industrial Parts & Fabrication Services'),
    ('LIGHTS & LIGHTING', 'Lights & Lighting'),
    ('LUGGAGE, BAGS & CASES', 'Luggage, Bags & Cases'),
    ('MACHINERY', 'Machinery'),
    ('MEASUREMENT & ANALYSIS INSTRUMENTS', 'Measurement & Analysis'),
    ('MINERALS & METALLURGY', 'Minerals & Metallurgy'),
    ('MULTIPLE PRODUCTS', 'Multiple Products'),
    ('OFFICE & SCHOOL SUPPLIES', 'Office & School Supplies'),
    ('PACKING & PRINTING', 'Packing & Printing'),
    ('RUBBER & PLASTICS', 'rubber & Plastics'),
    ('SECURITY & PROTECTION', 'Security & Protection'),
    ('SERVICE EQUIPMENT', 'Service Equipment'),
    ('SHOES & FOOTWEAR ACCESSORIES', 'Shoes & Footwear Accessories'),
    ('SPORTS & ENTERTAINMENT', 'Sports & Entertainment'),
    ('TELECOMMUNICATION', 'Telecommunication'),
    ('TEXTILE & LEATHER PRODUCT', 'Textile & Leather Product'),
    ('TIMEPIECES, JEWELRY , EYEWEAR', 'Timepieces, Jewelry , Eyewear'),
    ('TOOLS', 'Tools'),
    ('TOYS & HOBBIES', 'Toys & Hobbies'),
    ('TRANSPORTATION', 'Transportation'),
]

GENDER = [
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
]

STATUS = (
    (0, "Draft"),
    (1, "Publish"),
    (2, "Hold"),
)


class Proddisplay(models.Model):
    productname = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics', default='profile1.png')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.productname


class Rfq(models.Model):
    industry = models.CharField(max_length=100, choices=INDUSTRY, default='APPAREL')
    buyer_need = models.CharField(max_length=250)
    keywords = models.CharField(max_length=200)
    content = RichTextField(blank=True, null=True)
    qty_required = models.CharField(max_length=200)
    uom = models.CharField(max_length=200, choices=UOM)
    buying_frequency = models.CharField(max_length=200, choices=FREQUENCY1)
    image = models.ImageField(upload_to='pics', default='profile1.png')
    payment_mode = models.CharField(max_length=200, choices=PAYMENT)
    destination_port = models.CharField(max_length=200)
    time_validity = models.CharField(max_length=200, choices=FREQUENCY)
    updated_on = models.DateTimeField(auto_now=True, verbose_name="date updated")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    status = models.IntegerField(choices=STATUS, default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rfq')
    policy_agreed = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.buyer_need + '|' + str(self.author.email)


class RfqImage(models.Model):
    rfq = models.ForeignKey(Rfq, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.rfq.buyer_need


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, default='123456789')
    address = models.CharField(max_length=200, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Customer'

    def get_absolute_url(self):
        return reverse('customer-detail', args=[str(self.id)])

    class Meta:
        ordering = ['full_name']


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='pics', default='profile1.png')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(unique=True, null=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
            return '/'.join(full_path[::-1])

        return ' -> '.join(full_path[::-1])

    @property
    def get_products(self):
        return Product.objects.filter(category=self.title)

    class MPTTMeta:
        order_insertion_by = ['title']


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    keyfeatures = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products")
    marked_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = RichTextField(blank=True, null=True)
    warranty = models.CharField(max_length=300, null=True, blank=True)
    return_policy = models.CharField(max_length=300, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    offer = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="date published", null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    uom = models.CharField(max_length=200, choices=UOM, default="nos")
    noofpacksinonecartoon = models.PositiveIntegerField(default=0)
    moq = models.PositiveIntegerField(default=0)
    storagetemp = models.CharField(max_length=100, null=True, blank=True)
    shelflife = models.CharField(max_length=100, null=True, blank=True)
    rating = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=STATUS, default=0)
    show_product = models.BooleanField(default=False)
    policy_agreed = models.BooleanField(default=True)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.objects.all()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=(self.id,))

    def get_cat_list(self):
        k = self.category  # for now ignore this instance method

        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb) - 1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i - 1:-1])
        return breadcrumb[-1:0:-1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('slug', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'keyfeatures',
            'category',
            Row(
                Column('marked_price', css_class='form-group col-md-6 mb-0'),
                Column('selling_price', css_class='form-group col-md-4 mb-0'),
                Column('uom', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            'check_me_out',
            Submit('submit', 'Sign in')
        )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.product.title


class ProdComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prodcomment')
    name = models.CharField(max_length=80)
    mobile = models.CharField(max_length=80)
    email = models.EmailField()
    body = RichTextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti"),
    ("Esewa", "Esewa"),
)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(
        default=False, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)
