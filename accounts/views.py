from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView
import os
from django.conf import settings

from blog.models import Post
from buyerseller.models import Rfq, Customer, Order, Product, Category, Admin, ProdComment
from .forms import *
from django.contrib.auth.decorators import login_required

from .models import Profile, Contactme
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
import razorpay
from django.views.decorators.csrf import csrf_exempt

from verify_email.email_handler import send_verification_email


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


def update_user_data(user):
    Profile.objects.update_or_create(user=user, defaults={'mob': user.profile.mobile})
    Customer.objects.update_or_create(user=user, defaults={'username': user.customer.full_name})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            print(inactive_user)
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def adminprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile data has been updatedd!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    order = Post.objects.filter(author=request.user).order_by('-date_posted')
    paginator = Paginator(order, 6)
    page_number = request.GET.get('page')
    order_list = paginator.get_page(page_number)
    order = order_list
    rfq = Rfq.objects.filter(author=request.user).order_by('-created_on')
    paginator = Paginator(rfq, 6)
    page_number = request.GET.get('page')
    rfq_list = paginator.get_page(page_number)
    rfq = rfq_list

    product = Product.objects.filter(author=request.user).order_by('-created_on')
    paginator = Paginator(product, 6)
    page_number = request.GET.get('page')
    product_list = paginator.get_page(page_number)
    product = product_list

    myorders = Order.objects.filter(cart__customer=request.user.customer).order_by("-id")
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'orders': order,
        'rfq': rfq,
        'myorders': myorders,
        'product': product,
    }
    return render(request, 'accounts/adminprofile.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile data has been updatedd!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    order = Post.objects.filter(author=request.user).order_by('-date_posted')
    paginator = Paginator(order, 6)
    page_number = request.GET.get('page')
    order_list = paginator.get_page(page_number)
    order = order_list
    rfq = Rfq.objects.filter(author=request.user).order_by('-created_on')
    paginator = Paginator(rfq, 6)
    page_number = request.GET.get('page')
    rfq_list = paginator.get_page(page_number)
    rfq = rfq_list

    product = Product.objects.filter(author=request.user).order_by('-created_on')
    paginator = Paginator(product, 6)
    page_number = request.GET.get('page')
    product_list = paginator.get_page(page_number)
    product = product_list

    myorders = Order.objects.filter(cart__customer=request.user.customer).order_by("-id")
    ppostcount = Post.objects.filter(author=request.user).count()
    pproductcount = Product.objects.filter(author=request.user).count()
    pordercount = Order.objects.filter(customer=request.user.customer).count()
    pinquirycount = ProdComment.objects.filter(product__author=request.user).count()
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'orders': order,
        'rfq': rfq,
        'myorders': myorders,
        'product': product,
        'ppostcount': ppostcount,
        'pordercount': pordercount,
        'pproductcount': pproductcount,
        'pinquirycount': pinquirycount,
    }
    return render(request, 'profile.html', context)


@login_required
def myorganization(request):
    if request.method == 'POST':
        p_form = BussinessUpdateForm(request.POST,
                                     request.FILES,
                                     instance=request.user.profile)
        u_form = CompanyImageForm(request.POST,
                                  request.FILES,
                                  instance=request.user.profile)
        if u_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, f'Your profile data has been updatedd!')
            return redirect('profile')
    else:
        p_form = BussinessUpdateForm(instance=request.user.profile)
        u_form = CompanyImageForm(instance=request.user.profile)
    profile = Profile.objects.filter(user=request.user).order_by('-id')

    context = {
        'p_form': p_form,
        'u_form': u_form,
        'profile': profile,
    }
    return render(request, 'accounts/mybussiness.html', context)


@login_required
def myorder(request):
    order = Post.objects.filter(author=request.user).order_by('-date_posted')
    paginator = Paginator(order, 6)
    page_number = request.GET.get('page')
    order_list = paginator.get_page(page_number)
    order = order_list
    myorders = Order.objects.filter(cart__customer=request.user.customer).order_by("-id")
    context = {
        'orders': order,
        'myorders': myorders,
    }
    return render(request, 'accounts/myorders.html', context)


@login_required
def catalog(request):
    product = Product.objects.filter(author=request.user).order_by('-created_on')
    paginator = Paginator(product, 6)
    page_number = request.GET.get('page')
    product_list = paginator.get_page(page_number)
    product = product_list
    context = {
        'product': product,
    }
    return render(request, 'accounts/catalog.html', context)


def membership(request):
    return render(request, 'accounts/membership.html')


def myrfq(request):
    rfq = Rfq.objects.filter(author=request.user).order_by('-created_on')
    context = {
        'rfq': rfq,
    }
    return render(request, 'accounts/myrfq.html', context)


def mypost(request):
    ppost = Post.objects.filter(author=request.user).order_by('-created_on')
    ppostcount = Post.objects.filter(author=request.user).count()
    paginator = Paginator(ppost, 6)
    page_number = request.GET.get('page')
    post_list = paginator.get_page(page_number)
    context = {
        'post': post_list,
        'count': ppostcount,
    }
    return render(request, 'accounts/mypost.html', context)


def dashboard(request):
    context = {}
    return render(request, 'dashboard.html', context)


def transactions(request):
    context = {}
    return render(request, 'transactions.html', context)

def safedeal(request):
    context = {}
    return render(request, 'safedeal.html', context)


def policy(request):
    context = {}
    return render(request, 'accounts/privacypolicy.html', context)


def terms(request):
    context = {}
    return render(request, 'accounts/terms.html', context)


def faq1(request):
    filename = "faq.pdf"
    filepath = os.path.join(settings.MEDIA_ROOT, "goimex", filename)
    print(filepath)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')


def faq(request):
    context = {}
    return render(request, 'accounts/snippets/faq.html', context)


def success(request):
    context = {}
    return render(request, 'buyerseller/rfqsuccess.html', context)


def listing(request):
    context = {}
    return render(request, 'accounts/listingpolicy.html', context)


def buyerjoining(request):
    context = {}
    return render(request, 'accounts/buyerjoining.html', context)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    template_name = "accounts/category.html"
    form_class = CategoryForm
    success_url = reverse_lazy("admincategorylist")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AdminCategoryListView(AdminRequiredMixin, ListView):
    template_name = "accounts/admincategorylist.html"
    queryset = Category.objects.all().order_by("-id")
    context_object_name = "allcat"

    def get_context_data(self, **kwargs):
        context = super(AdminCategoryListView, self).get_context_data(**kwargs)
        allcat = Category.objects.all().order_by("-id")
        paginator = Paginator(allcat, 5)
        page_number = self.request.GET.get('page')
        cat_list = paginator.get_page(page_number)
        context['allcat'] = cat_list
        return context


@login_required(login_url='login')
def contact(request):
    if request.method == "POST":
        input_name = request.POST['input_name']
        contact_input_email = request.POST['contact_input_email']
        contact_input_subject = request.POST['contact_input_subject']
        contact_input_mobile = request.POST['contact_input_mobile']
        contact_input = request.POST['contact_input']
        mobile = request.POST['contact_input_mobile']
        subject = "Thank you for contacting Goimex.com."
        message = "Dear " + input_name + ",\n\n" \
                  + "We will get in touch with you soon." + "\n\n\n" \
                  + "Your message details : -" + "\n" \
                  + "Message From-" + input_name + "\n" \
                  + "Email:-" + contact_input_email + "\n\n" \
                  + "Mobile:-" + mobile + "\n\n" \
                  + "Subject-" + contact_input_subject + "\n\n" \
                  + "Details-" + contact_input + "\n\n\n" \
                  + "Warm Regards \n\n From: Goimex Support Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [contact_input_email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        name = request.POST['input_name']
        email = request.POST['contact_input_email']
        subject = request.POST['contact_input_subject']
        message = request.POST['contact_input']
        contactme = Contactme(name=name, email=email, mobile=mobile, subject=subject, message=message)
        contactme.save()
        dest = Contactme.objects.filter(name=name, email=email, mobile=mobile, message=message).order_by('-id')[:1]

        context = {
            'contact_input_name': input_name,
            'dest': dest,
            'header': 'Contact',

        }
        return render(request, 'contact.html', context)
    else:
        context = {
        }
        return render(request, "contact.html", context)


@login_required(login_url='login')
def basicpayment(request):
    keyid = 'rzp_live_8iKdUKGqRVttUs'
    keySecret = 'utpgdTG6iY9OXcRVwZ6pepLu'
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 999900
        client = razorpay.Client(
            auth=(keyid, keySecret))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
    return render(request, 'accounts/payment.html')


def silverpayment(request):
    keyid = 'rzp_live_8iKdUKGqRVttUs'
    keySecret = 'utpgdTG6iY9OXcRVwZ6pepLu'
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 1899900
        client = razorpay.Client(
            auth=(keyid, keySecret))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
    return render(request, 'accounts/payment1.html')


def goldpayment(request):
    keyid = 'rzp_live_8iKdUKGqRVttUs'
    keySecret = 'utpgdTG6iY9OXcRVwZ6pepLu'
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 3699900
        client = razorpay.Client(
            auth=(keyid, keySecret))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
    return render(request, 'accounts/payment2.html')


def paltpayment(request):
    keyid = 'rzp_live_8iKdUKGqRVttUs'
    keySecret = 'utpgdTG6iY9OXcRVwZ6pepLu'
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 5499900
        client = razorpay.Client(
            auth=(keyid, keySecret))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
        client = razorpay.Client(auth=(os.getenv('razorpaykey'), os.getenv('razorpaysecret')))
        response = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 1})
        print(response)
        context = {'response': response}
    return render(request, 'accounts/payment3.html')


def expayment(request):
    keyid = 'rzp_live_8iKdUKGqRVttUs'
    keySecret = 'utpgdTG6iY9OXcRVwZ6pepLu'
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 8199900
        client = razorpay.Client(
            auth=(keyid, keySecret))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
    return render(request, 'accounts/payment4.html')


@csrf_exempt
def success(request):
    return render(request, "success.html")
