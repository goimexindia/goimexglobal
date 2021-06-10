from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    UpdateView,
    UpdateView,
    UpdateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import hierarchy as hierarchy

from accounts.models import Profile
from .models import Post, PostImage
from buyerseller.models import Rfq, Category, Admin, Customer, Product
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from .forms import CommentForm, ImageForm, PostForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


def home(request):
    catlist = Post.objects.all().distinct('category')
    category = Category.objects.all()
    suppliers = Profile.object.all()
    search_post = request.GET.get('search')
    if search_post:
        posts = Post.objects.exclude(posttype='buyer').filter(status=1).filter(
            Q(title__icontains=search_post) & Q(content__icontains=search_post))
    else:
        # posts = Post.objects.all().order_by("-date_posted")
        posts = Post.objects.exclude(posttype='buyer').filter(status=1).order_by('-id')

    paginator = Paginator(posts, 5)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/home.html',
                  {'posts': post_list, 'page': page, 'suppliers': suppliers, 'category': category, 'catlist': catlist})


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    category = Post.objects.values('category').distinct()
    category = Post.objects.all().distinct('category')
    return render(request, 'buyerseller/categories.html', {'cats': cats, 'posts': category_posts, 'catlist': category})


def ProductCategoryView(request, cats):
    category_posts = Product.objects.filter(category=cats, status=1)
    category = Product.objects.values('category').distinct()
    category = Product.objects.filter(status=1).distinct('category')
    return render(request, 'buyerseller/productcategories.html',
                  {'cats': cats, 'product_list': category_posts, 'catlist': category})


def search(request):
    catlist = Post.objects.all().distinct('category')
    search_post = request.GET.get('search')
    type_post = request.GET.get('type')

    profile = Profile.objects.filter(Q(organization__icontains=search_post) | Q(products__icontains=search_post))

    if search_post:
        posts = Post.objects.filter(
            Q(title__icontains=search_post) |
            Q(snippet__icontains=search_post)).exclude(posttype='service')
    else:
        posts = Post.objects.filter(status=1).exclude(posttype='service').order_by("-date_posted")

    if type_post == 'service':
        posts = Post.objects.filter(posttype='service', status=1).filter(
            Q(title__icontains=search_post) |
            Q(snippet__icontains=search_post)).order_by("-date_posted")

    paginator = Paginator(posts, 5)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    if type_post == 'manufacturer':
        profile = Profile.objects.filter(Q(organization__icontains=search_post) | Q(products__icontains=search_post)).filter(type='manufacturer')
        return render(request, 'blog/allcompany.html',
                      {'posts': post_list, 'catlist': catlist, 'profile': profile, 'page': page, 'type': type_post})
    if type_post == 'company':
        profile = Profile.objects.filter(Q(organization__icontains=search_post) | Q(products__icontains=search_post)).exclude(type='manufacturer')
        return render(request, 'blog/allcompany.html',
                      {'posts': post_list, 'catlist': catlist, 'profile': profile, 'page': page, 'type': type_post})
    if type_post == 'buyer':
        return render(request, 'blog/homepostbuy.html',
                      {'posts': post_list, 'catlist': catlist, 'page': page, 'type': type_post})
    else:
        return render(request, 'blog/home.html',
                      {'posts': post_list, 'catlist': catlist, 'page': page, 'type': type_post})


class PostSearchListView(ListView):
    """
    Display a Blog List page filtered by the search query.
    """
    model = Post
    paginate_by = 10

    def get_queryset(self):
        qs = Post.objects.published()

        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            title_vector = SearchVector('title', weight='A')
            content_vector = SearchVector('content', weight='B')
            vectors = title_vector + content_vector
            qs = qs.annotate(search=vectors).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vectors, query)).order_by('-rank')

        return qs


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    posts = Post.objects.exclude(posttype='buyer').filter(status=1).order_by('-id')
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.exclude(posttype='buyer').filter(status=1).order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        postss = Post.objects.exclude(posttype='buyer').filter(status=1).order_by('-id')
        catlist = Post.objects.all().distinct('category')
        paginator = Paginator(postss, 5)
        page_number = self.request.GET.get('page')
        post_list = paginator.get_page(page_number)
        context['posts'] = post_list
        context['catlist'] = catlist
        return context


class BuyerPostListView(ListView):
    model = Post
    template_name = 'blog/homepostbuy.html'  # <app>/<model>_<viewtype>.html
    posts = Post.objects.exclude(posttype='seller').filter(status=1).order_by('-id')
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.exclude(posttype='seller').filter(status=1).order_by('-id')

    def get_context_data(self, *args, **kwargs):
        categorylist = Post.objects.all().distinct('category')
        context = super(BuyerPostListView, self).get_context_data(**kwargs)
        posts = Post.objects.exclude(posttype='seller').filter(status=1).order_by('-id')
        paginator = Paginator(posts, 5)
        page_number = self.request.GET.get('page')
        post_list = paginator.get_page(page_number)
        context['posts'] = post_list
        context['catlist'] = categorylist
        return context


class ServicePostListView(ListView):
    model = Post
    template_name = 'blog/homepostbuy.html'  # <app>/<model>_<viewtype>.html
    posts = Post.objects.filter(posttype='service').filter(status=1).order_by('-id')
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(posttype='service').filter(status=1).order_by('-id')

    def get_context_data(self, *args, **kwargs):
        categorylist = Post.objects.all().distinct('category')
        context = super(ServicePostListView, self).get_context_data(**kwargs)
        posts = Post.objects.filter(posttype='service').filter(status=1).order_by('-id')
        paginator = Paginator(posts, 5)
        page_number = self.request.GET.get('page')
        post_list = paginator.get_page(page_number)
        context['posts'] = post_list
        context['catlist'] = categorylist
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user, status=1).order_by('-date_posted')


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        cat = get_object_or_404(User, category=self.kwargs.get('category'))
        return Post.objects.filter(category=cat, status=1).order_by('-date_posted')


def detail_views(request, id):
    post = get_object_or_404(Post, id=id)
    photos = PostImage.objects.filter(post=post)
    return render(request, 'detail.html', {
        'post': post,
        'photos': photos
    })


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        posts = get_object_or_404(Post, id=self.kwargs['pk'])
        photos = PostImage.objects.filter(post=posts)
        posts.view_count += 1
        posts.save()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["liked"] = liked
        context["photos"] = photos
        context['posts'] = posts
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "blog/post_form.html"
    form_class = PostForm
    success_url = '/blog'

    def form_valid(self, form):
        form.instance.author = self.request.user
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            PostImage.objects.create(post=p, images=i)
        return super().form_valid(form)


class PostDeleteView(AdminRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUpdateView(AdminRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'title_tag', 'category', 'image', 'content', 'snippet', 'status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        rfq = self.get_object()
        if self.request.user == rfq.author:
            return True
        return False


def categories(request):
    category_slug = hierarchy.split('/')
    category_queryset = list(Category.objects.all())
    all_slugs = [x.slug for x in category_queryset]
    parent = None
    for slug in category_slug:
        if slug in all_slugs:
            parent = get_object_or_404(Category, slug=slug, parent=parent)
        else:
            instance = get_object_or_404(Post, slug=slug)
            breadcrumbs_link = instance.get_cat_list()
            category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
            breadcrumbs = zip(breadcrumbs_link, category_name)
            return render(request, "postDetail.html", {'instance': instance, 'breadcrumbs': breadcrumbs})

    return render(request, "buyseller/categories.html",
                  {'post_set': parent.post_set.all(), 'sub_categories': parent.children.all()})


def about(request):
    return render(request, 'blog/about.html', {'title': 'ABOUT'})


def aboutus(request):
    return render(request, 'buyerseller/aboutus.html', {'title': 'ABOUT US'})


def new(request):
    return render(request, 'new11.html', {'title': 'NEW'})


def logout(request):
    return render(request, 'blog/about.html', {'title': 'ABOUT'})


def pt(request, slug):
    template_name = 'blog/pt.html'
    post = get_object_or_404(Post, id=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def like(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Post.objects.filter(
            Q(tittle_icontains=q) |
            Q(content_icontains=Q)
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))


class AdminPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/adminpostlist.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'allproducts'
    paginate_by = 5


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def allcompany(request):
    search_post = request.GET.get('search')
    if search_post:
        profile = Profile.objects.filter(Q(organization__icontains=search_post) | Q(products__icontains=search_post))
    else:
        profile = Profile.objects.exclude(organization__isnull=True).exclude(type='manufacturer').order_by("-id")
    return render(request, 'blog/allcompany.html', {'profile': profile})


def mfgcompany(request):
    search_post = request.GET.get('search')
    if search_post:
        profile = Profile.objects.filter(Q(organization__icontains=search_post) | Q(products__icontains=search_post))
    else:
        profile = Profile.objects.exclude(organization__isnull=True).filter(type='manufacturer').order_by("-id")
    return render(request, 'blog/allcompany.html', {'profile': profile})
