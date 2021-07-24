from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import *

urlpatterns = [
    path("home", HomeView.as_view(), name="home"),
    path('cat1/<str:slug>/', ItemsByCategoryView.as_view(), name='category-detail'),
    path("apphome", HomeAppView.as_view(), name="apphome"),
    path("", NewAppView.as_view(), name="newhome"),
    path('catsearch/', views.catsearch, name='cat-search'),
    path('categorylist', CategoryListView.as_view(), name='category-list'),
    url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
    path('adminpostsearch/', views.adminpostsearch, name='adminpost-search'),
    path("ecomerce", EcomerceView.as_view(), name="ecomerce"),
    path("ecomerceapp", EcomerceAppView.as_view(), name="ecomerceapp"),
    path("all-products/", AllProductsView.as_view(), name="allproducts"),
    path("all-essentials/", EssentialsView.as_view(), name="allessentials"),
    path('Cart/new/', CartCreateView.as_view(), name='cart-create'),
    path('Cart/<int:pk>/update', CartUpdateView.as_view(), name='cart-update'),
    path('product/<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('Cart/<int:pk>/delete', CartDeleteView.as_view(), name='cart-delete'),
    path('htscode', views.htscode, name='htscode'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('companyproduct/<int:pk>/', views.companyproduct, name='companyproduct'),
    path('customer/<int:pk>/', views.customer, name='customer'),
    path('cat/list/', Cat.as_view(), name='cat'),
    path('prodcomment/<slug:slug>/', views.prodcomment, name='prodcomment'),
    path('prodinquiry/<slug:slug>/', views.prodinquiry, name='prodinquiry'),
    path('rfq', RfqCreateView.as_view(), name='rfq'),
    path('safedealform', SafedealCreateView.as_view(), name='safedealform'),
    path('rfq/<int:pk>/update', RfqUpdateView.as_view(), name='rfq-update'),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),
    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(),
         name="customerorderdetail"),
    path('productsearch/', views.productsearch, name='productsearch'),
    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),
    path("admin-home/", AdminHomeView.as_view(), name="adminhome"),
    path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(),
         name="adminorderdetail"),
    path("admin-all-rfq/", AdminrfqListView.as_view(), name="adminrfqlist"),
    path("admin-all-orders/", AdminOrderListView.as_view(), name="adminorderlist"),
    path("admin-all-posts/", AdminPostListView.as_view(), name="adminpostlist"),
    path("admin-order-<int:pk>-change/",
         AdminOrderStatuChangeView.as_view(), name="adminorderstatuschange"),

    path("admin-product/add/", AdminProductCreateView.as_view(),
         name="adminproductcreate"),

    path("admin-product/list/", AdminProductListView.as_view(),
         name="adminproductlist"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
