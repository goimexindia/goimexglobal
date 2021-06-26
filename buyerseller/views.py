import hierarchy as hierarchy
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views import View, generic
from django.views.generic import TemplateView, FormView
from django.contrib.auth import authenticate, login
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from mptt.forms import TreeNodeChoiceField

from .filters import OrderFilter
from blog.models import Post
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import *
import requests
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q


class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        prod = Proddisplay.objects.all().order_by("-id")
        category = Category.objects.all()
        suppliers = Profile.objects.exclude(organization__isnull=True).exclude(type='Buyer').order_by("-id")[:12]
        products = Product.objects.all().order_by("-id")[:12]
        topproducts = Product.objects.distinct('category').order_by("category")[:12]
        productss = Product.objects.all().exclude(image__isnull=True).order_by("-id")[:12]
        post = Post.objects.all().order_by("-id")
        context['prod'] = prod
        context['suppliers'] = suppliers
        context['topproducts'] = topproducts
        context['products'] = products
        context['productss'] = productss
        context['post'] = post
        context['category'] = category
        paginator = Paginator(products, 12)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['products'] = product_list
        return context


class HomeAppView(TemplateView):
    template_name = "index1.html"

    def get_context_data(self, **kwargs):
        context = super(HomeAppView, self).get_context_data(**kwargs)
        prod = Proddisplay.objects.all().order_by("-id")
        category = Category.objects.all()
        suppliers = Profile.objects.exclude(organization__isnull=True).exclude(type='Buyer').order_by("-id")[:12]
        products = Product.objects.all().order_by("-id")[:12]
        topproducts = Product.objects.distinct('category').order_by("category")[:12]
        productss = Product.objects.all().exclude(image__isnull=True).order_by("-id")[:12]
        post = Post.objects.all().order_by("-id")
        context['prod'] = prod
        context['suppliers'] = suppliers
        context['topproducts'] = topproducts
        context['products'] = products
        context['productss'] = productss
        context['post'] = post
        context['category'] = category
        paginator = Paginator(products, 12)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['products'] = product_list
        return context


class EcomerceView(TemplateView):
    template_name = "buyerseller/ecomerce.html"

    def get_context_data(self, **kwargs):
        context = super(EcomerceView, self).get_context_data(**kwargs)
        all_products = Product.objects.filter(status=1).order_by("-id")
        paginator = Paginator(all_products, 20)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context


class EcomerceAppView(TemplateView):
    template_name = "buyerseller/ecomerceapp.html"

    def get_context_data(self, **kwargs):
        context = super(EcomerceAppView, self).get_context_data(**kwargs)
        all_products = Product.objects.filter(status=1).order_by("-id")
        paginator = Paginator(all_products, 20)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context


class AllProductsView(TemplateView):
    template_name = "buyerseller/allproducts.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['allcategories'] = Category.objects.all()
        categoryid = self.request.GET.get('category')
        if categoryid:
            context['allcategories'] = Category.objects.filter(category=categoryid)
        return context


class EssentialsView(TemplateView):
    template_name = "essentials.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['allcategories'] = Category.objects.all()
        categoryid = self.request.GET.get('category')
        if categoryid:
            context['allcategories'] = Category.objects.filter(category=categoryid)
        return context


def catsearch(request):
    search_product = request.GET.get('search')
    if search_product:
        product = Product.objects.filter(Q(title__icontains=search_product) |
                                         Q(description__icontains=search_product))
    else:
        product = Product.objects.all().order_by("-created_on")
    paginator = Paginator(product, 20)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        product_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        product_list = paginator.page(paginator.num_pages)
    return render(request, 'buyerseller/ecomerce.html', {'product_list': product_list, 'page': page})


class ProductDetailView(TemplateView):
    template_name = "buyerseller/productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context


class AddToCartView(EcomMixin, TemplateView):
    template_name = "buyerseller/addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']

        # get product
        product_obj = Product.objects.get(id=product_id)
        author = product_obj.author
        context['author'] = author
        sameuser = Product.objects.filter(author=author)
        context['sameuser'] = sameuser
        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1,
                    subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1,
                subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart

        return context


class MyCartView(EcomMixin, TemplateView):
    template_name = "buyerseller/mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("mycart")


class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("mycart")


class CheckoutView(EcomMixin, CreateView):
    template_name = "buyerseller/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("ecomerce")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.customer = self.request.user.customer
            form.instance.order_status = "Order Received"
            form.instance.author = self.request.user
            p = form.save()
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("payment_method")
            order = form.save()
            if pm == "Khalti":
                return redirect(reverse("khaltirequest") + "?o_id=" + str(order.id))
            elif pm == "Esewa":
                return redirect(reverse("esewarequest") + "?o_id=" + str(order.id))
        else:
            return redirect("ecomerce")
        return super().form_valid(form)


def product(request):
    return render(request, 'buyerseller/product.html')


def htscode(request):
    return render(request, 'buyerseller/htscode.html')


def aboutus(request):
    return render(request, 'buyerseller/aboutus.html')


def companyproduct(request, pk):
    author = User.objects.get(id=pk)
    product = author.product_set.filter(status=1)

    post = Post.objects.filter(author=author, status=1)

    productall = author.product_set.filter(status=1)
    paginator = Paginator(product, 5)
    page = request.GET.get('page')
    try:
        list_product = paginator.page(page)
    except PageNotAnInteger:
        list_product = paginator.page(1)
    except EmptyPage:
        list_product = paginator.page(paginator.num_pages)
    context = {'profiles': author, 'product': list_product, 'page': page, 'productall': productall, 'post': post}
    return render(request, 'buyerseller/companyinfo.html', context, )


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

    return render(request, "categories.html",
                  {'post_set': parent.post_set.all(), 'sub_categories': parent.children.all()})


class RfqCreateView(LoginRequiredMixin, CreateView):
    template_name = "buyerseller/rfqcreate.html"
    form_class = RfqForm
    success_url = '/accounts/success'

    def form_valid(self, form):
        form.instance.author = self.request.user
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            RfqImage.objects.create(rfq=p, image=i)
        return super().form_valid(form)


class RfqUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Rfq
    template_name = 'buyerseller/rfqcreate.html'
    fields = ['industry', 'buyer_need', 'keywords', 'content', 'qty_required', 'uom',
              'buying_frequency', 'image', 'payment_mode', 'destination_port', 'time_validity']
    success_url = '/blog'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CustomerOrderDetailView(DetailView):
    template_name = "buyerseller/customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect("profile")
        else:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)


def show_category(request, hierarchy=None):
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

    return render(request, "categories.html",
                  {'post_set': parent.post_set.all(), 'sub_categories': parent.children.all()})


class CartCreateView(LoginRequiredMixin, CreateView):
    template_name = "buyerseller/cart_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecomerce")

    def form_valid(self, form):
        form.instance.author = self.request.user
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        return super().form_valid(form)


class ProductUpdateView(AdminRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "buyerseller/product_form.html"
    model = Product
    fields = '__all__'
    success_url = reverse_lazy("adminhome")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if AdminRequiredMixin:
            return True
        return False


class CartUpdateView(AdminRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "buyerseller/cart_form.html"
    model = Product
    fields = ["title", "slug", "keyfeatures", "category", "image", "marked_price",
              "selling_price", "description", "warranty", "return_policy", "offer"]
    success_url = reverse_lazy("ecomerce")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        rfq = self.get_object()
        if AdminRequiredMixin:
            return True
        return False


class CartDeleteView(AdminRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "buyerseller/product_confirm_delete.html"
    model = Product
    success_url = '/ecomerce'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class AdminLoginView(FormView):
    template_name = "accounts/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "accounts/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pendingorders = Order.objects.filter(
            order_status="Order Received").order_by("-id")
        paginator = Paginator(pendingorders, 5)
        page_number = self.request.GET.get('page')
        order_list = paginator.get_page(page_number)
        context["pendingorders"] = order_list

        pendingproduct = Product.objects.filter(
            status=0).order_by("-id")
        paginator = Paginator(pendingproduct, 5)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context["pendingproduct"] = product_list

        pendingpost = Post.objects.filter(
            status=0).order_by("-id")
        paginator = Paginator(pendingpost, 5)
        page_number = self.request.GET.get('page')
        post_list = paginator.get_page(page_number)
        context["allpost"] = post_list

        return context


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "accounts/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context


class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "accounts/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"

    def get_context_data(self, **kwargs):
        context = super(AdminOrderListView, self).get_context_data(**kwargs)
        allorders = Order.objects.all().order_by("-id")
        paginator = Paginator(allorders, 8)
        page_number = self.request.GET.get('page')
        order_list = paginator.get_page(page_number)
        context['allorders'] = order_list
        return context


class AdminPostListView(AdminRequiredMixin, ListView):
    template_name = "accounts/adminpostlist.html"
    queryset = Post.objects.all().order_by("-id")
    context_object_name = "allposts"

    def get_context_data(self, **kwargs):
        context = super(AdminPostListView, self).get_context_data(**kwargs)
        allpost = Post.objects.all().order_by("-id")
        paginator = Paginator(allpost, 8)
        page_number = self.request.GET.get('page')
        post_list = paginator.get_page(page_number)
        context['allposts'] = post_list
        return context


class AdminrfqListView(AdminRequiredMixin, ListView):
    template_name = "accounts/adminrfqlist.html"
    queryset = Rfq.objects.all().order_by("-id")
    context_object_name = "allrfq"

    def get_context_data(self, **kwargs):
        context = super(AdminrfqListView, self).get_context_data(**kwargs)
        allrfq = Rfq.objects.all().order_by("-id")
        paginator = Paginator(allrfq, 8)
        page_number = self.request.GET.get('page')
        rfq_list = paginator.get_page(page_number)
        context['allrfq'] = rfq_list
        return context


class AdminOrderStatuChangeView(AdminRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("adminorderdetail", kwargs={"pk": order_id}))


class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = "accounts/adminproductlist.html"
    queryset = Product.objects.all().order_by("-id")
    context_object_name = "allproducts"

    def get_context_data(self, **kwargs):
        context = super(AdminProductListView, self).get_context_data(**kwargs)
        allproduct = Product.objects.all().order_by("-id")
        paginator = Paginator(allproduct, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['allproducts'] = product_list
        return context


def productsearch(request):
    search_product = request.GET.get('search')
    if search_product:
        product = Product.objects.filter(Q(title__icontains=search_product) |
                                         Q(description__icontains=search_product))
    else:
        product = Product.objects.all().order_by("-created_on")

    paginator = Paginator(product, 5)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'accounts/adminproductlist.html', {'allproducts': post_list, 'page': page})


class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "accounts/adminproductcreate.html"
    form_class = ProductForm
    success_url = reverse_lazy("adminproductlist")

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        return super().form_valid(form)


def cat(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();

    data = {}
    data['products'] = products
    search_post = request.GET.get('search')
    if search_post:
        data = {}
        products = Product.objects.filter(Q(title__icontains=search_post))
        data['products'] = products
    data['categories'] = Category.get_all_categories()
    print('you are : ', request.session.get('email'))
    return render(request, 'buyerseller/productcategory.html', data)


class Cat(TemplateView):
    template_name = "buyerseller/productcategory.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        categoryID = self.request.GET.get('category')
        categories = Category.objects.all()
        products = Product.get_all_products()
        context['products'] = products
        context['categories'] = categories
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        paginator = Paginator(products, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['products'] = product_list
        context['category'] = categories
        context['categories'] = categories
        return context


def prodcomment(request, slug):
    template_name = 'buyerseller/prodcomment.html'
    product = get_object_or_404(Product, id=slug)
    comments = product.prodcomment.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = ProdCommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.product = product
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = ProdCommentForm()

    return render(request, template_name, {'product': product,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def prodinquiry(request, slug):
    template_name = 'buyerseller/prodinquiry.html'
    product = get_object_or_404(Product, id=slug)
    comments = product.prodcomment.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = ProdInquiryForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.product = product
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = ProdInquiryForm()

    return render(request, template_name, {'product': product,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def companycomment(request, slug):
    template_name = 'buyerseller/companycomment.html'
    product = get_object_or_404(Product, id=slug)
    comments = product.prodcomment.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = ProdCommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.product = product
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = ProdCommentForm()

    return render(request, template_name, {'product': product,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def catsearch(request):
    search_product = request.GET.get('search')

    if search_product:
        product = Product.objects.filter(Q(title__icontains=search_product) |
                                         Q(description__icontains=search_product))
    else:
        product = Product.objects.filter(status=1).order_by("-created_on")

    paginator = Paginator(product, 20)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        product_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        product_list = paginator.page(paginator.num_pages)

    return render(request, 'buyerseller/ecomerce.html', {'product_list': product_list, 'page': page})


def adminpostsearch(request):
    search_post = request.GET.get('search')
    if search_post:
        post = Post.objects.filter(Q(title__icontains=search_post) |
                                   Q(content__icontains=search_post))
    else:
        post = Post.objects.all().order_by("-id")

    paginator = Paginator(post, 8)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'accounts/adminpostlist.html', {'allposts': post_list, 'page': page})


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    myFilter = OrderFilter(request.GET, queryset=orders)
    tableFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'orders': orders, 'tableFilter': tableFilter, }
    return render(request, 'accounts/customer.html', context)


class ProductListView(generic.ListView):
    model = Product

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ProductListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class CategoryListView(generic.ListView):
    model = Category
    template_name = "buyseller/category_list.html"


class SafedealCreateView(LoginRequiredMixin, CreateView):
    template_name = "buyerseller/safedealcreate.html"
    form_class = SafedealForm
    success_url = '/accounts/success'

    def form_valid(self, form):
        form.instance.author = self.request.user
        p = form.save()
        return super().form_valid(form)
