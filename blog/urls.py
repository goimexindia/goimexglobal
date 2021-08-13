from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('buyerpost', BuyerPostListView.as_view(), name='blog-buyerhome'),
    path('buyerpostapp', AppBuyerPostListView.as_view(), name='blog-buyerhomeapp'),
    path('servicepost', ServicePostListView.as_view(), name='blog-servicehome'),
    path('allcompany', views.allcompany, name='allcompany'),
    path('mfgcompany', views.mfgcompany, name='mfgcompany'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # path('category/<str:category>', CategoryPostListView.as_view, name='category-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('postapp/<int:pk>/', PostDetailViewapp.as_view(), name='post-detailapp'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='blog-about'),
    path('aboutus/', views.aboutus, name='blog-aboutus'),
    path('new/', views.new, name='blog-new'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='blog-search'),
    path('searchapp/', views.searchapp, name='blog-searchapp'),
    path('pt/<slug:slug>/', views.pt, name='pt'),
    path('like/<int:pk>', views.like, name='like'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('productcategory/<str:cats>/', ProductCategoryView, name='productcategory'),
    path('<int:id>/', views.detail_views, name='detail'),
    path("post/list/", AdminPostListView.as_view(),
         name="adminpostlist"),

]
