from datetime import datetime, timedelta

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, FormView

from apps.mixins import NotLoginRequiredMixin

from apps.forms import RegisterForm
from apps.models import Blog, Comment, Category, Shop, Blog

# def blog_list_page(request):
#     context = {
#         'blogs': Blog.objects.all()
#
#     }
#     return render(request, 'apps/blogs/blog_list.html', context)
from apps.utils import send_email


class BlogListView(ListView):
    paginate_by = 3
    template_name = 'apps/blogs/blog_list.html'
    queryset = Blog.objects.order_by('-id')
    context_object_name = 'blogs'


# def blog_detile(request, pk):
#     context = {
#         'blog': Blog.objects.filter(pk=pk).first(),
#         'comments': Comment.objects.all(),
#
#     }
#     return render(request, 'apps/blogs/blog_detiles.html', context)

class BlogDetailWiew(DetailView):
    template_name = 'apps/blogs/blog_detiles.html'
    queryset = Blog.objects.order_by('-created_at')
    pk_url_kwarg = 'pk'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_blogs'] = self.get_queryset()[:3]
        return context


# def index(request):
#     return render(request, 'apps/index.html')

class IndexView(TemplateView):
    template_name = 'apps/index.html'


# def logout_(request):
#     logout(request)
#     return redirect('index')


# def login_page(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request,user)
#             return redirect('index')
#
#     return render(request, 'apps/login.html')

class CustomLoginView(NotLoginRequiredMixin, LoginView):
    template_name = 'apps/login.html'


# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#
#     return render(request, 'apps/register.html')

class RegisterFormView(FormView):
    template_name = 'apps/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        print('12')
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for i in form.errors:
            print(i)
        return super().form_valid(form)


# def shop_list(request):
#     context = {
#         'blogs': Blog.objects.all()
#
#     }
#     return render(request, 'apps/shop/shop_list.html', context)

class ShopListView(TemplateView):
    template_name = 'apps/shop/shop_list.html'
    queryset = Shop.objects.all()
    context_object_name = 'shops'

    def created(self):
        current_date = datetime.now().date()
        last_7_days = current_date - timedelta(days=7)
        return last_7_days
