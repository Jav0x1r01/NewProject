from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import IndexView, RegisterFormView, ShopListView, CustomLoginView, BlogListView, BlogDetailWiew

urlpatterns = [
    path('login', CustomLoginView.as_view(success_url='index'), name='login'),
    path('', IndexView.as_view(), name='index'),
    path('register', RegisterFormView.as_view(), name='register_page'),
    path('blog_detile/<int:pk>', BlogDetailWiew.as_view(), name='blog_detile'),
    path('shop_list', ShopListView.as_view(), name='shop_list'),
    path('blog_list', BlogListView.as_view(), name='blog_list'),
    path('logout', LogoutView.as_view(next_page='index'), name='logout_'),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),

]







