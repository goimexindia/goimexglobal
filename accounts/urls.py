from django.urls import path

from . import views
from .views import CategoryCreateView, AdminCategoryListView

urlpatterns = [
    path('register', views.register, name='register'),
    path('basicpayement', views.basicpayment, name='basicpayment'),
    path('silverpayement', views.silverpayment, name='silverpayment'),
    path('goldpayement', views.goldpayment, name='goldpayment'),
    path('paltpayement', views.paltpayment, name='paltpayment'),
    path('expayement', views.expayment, name='expayment'),
    path('success', views.success, name='success'),
    path('login', views.login, name='login'),
    path('contact', views.contact, name='contact'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('faq', views.faq, name='faq'),
    path('buyerjoining', views.buyerjoining, name='buyerjoining'),
    path('mybussiness', views.myorganization, name='mybussiness'),
    path('catalog', views.catalog, name='catalog'),
    path('membership', views.membership, name='membership'),
    path('myrfq', views.myrfq, name='myrfq'),
    path('mypost', views.mypost, name='mypost'),
    path('admincat', CategoryCreateView.as_view(), name='admincat'),
    path('admin-all-category', AdminCategoryListView.as_view(), name="admincategorylist"),
    path('myorder', views.myorder, name='myorder'),
    path('adminprofile', views.adminprofile, name='adminprofile'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('policy', views.policy, name='policy'),
    path('terms', views.terms, name='terms'),
    path('success', views.success, name='success'),
    path('listing', views.listing, name='listing'),
    path('transactions', views.transactions, name='transactions'),
    path('safedeal', views.safedeal, name='safedeal'),
]
