from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image

STATUS = (
    (0, "Draft"),
    (1, "Publish"),
    (2, "Hold"),
)
TYPE_CHOICES = [
    ("buyer", "Buyer"),
    ("seller", "Seller"),
    ("retailer", "Retailer"),
    ("agent", "Agent"),
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


def upload_location(instance, filename, **kwargs):
    file_path = 'blog/{author_id}/{title)-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    title_tag = models.SlugField(max_length=200, default='Enter Keywords separated by comas. Eg.:cars, bikes')
    image = models.ImageField(upload_to='pics', default='profile1.png')
    content = RichTextField(default="Dear Sir/Madam,I am looking for products with the following specifications:-")
    category = models.CharField(max_length=100, choices=INDUSTRY, default='APPAREL')
    snippet = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goimex_posts')
    updated_on = models.DateTimeField(auto_now=True, verbose_name="date updated")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    view_count = models.PositiveIntegerField(default=0)
    posttype = models.CharField(max_length=50, choices=TYPE_CHOICES, default="buyer", verbose_name="request type")

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + '|' + str(self.author)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_blog_post_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_blog_post_receiever, sender=Post)


class PostImage(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to='blog/')

    def __str__(self):
        return self.post.title

    def save(self, *args, **kwargs):
        super().save()
        images = Image.open(self.images.path)
        if images.height > 400 or images.width > 600:
            output_size = (400, 600)
            images.thumbnail(output_size)
            images.save(self.images.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    mobile = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
