import time
import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, ForeignKey, CASCADE, DateTimeField, ImageField, ManyToManyField, \
    FloatField, UUIDField, EmailField
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField
from apps.tasks import task_send_email


class Category(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(Model):
    name = CharField(max_length=255)
    author = ForeignKey('apps.User', CASCADE, 'blogs')
    category = ForeignKey('apps.Category', CASCADE)
    image = ImageField(default='blog/defoult.png', upload_to='blog/images/')
    tags = ManyToManyField('apps.Tag')
    text = CKEditor5Field(blank=True, null=True, config_name='extends')
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        emails: list = Email.objects.values_list('email', flat=True)
        start = time.time()
        task_send_email.delay("Yangi blog qoshildi", self.name, list(emails))
        end = time.time()
        print(end - start, ' s -- ketgan vaqt')
        print(list(emails))

    def count_comment(self):
        return self.comment_set.count()

    def __str__(self):
        return self.name


class Comment(Model):
    text = CharField(max_length=255)
    Blog = ForeignKey('apps.Blog', CASCADE)
    author = ForeignKey('apps.User', CASCADE, 'comments')
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class User(AbstractUser):
    image = ResizedImageField(size=[90, 90], crop=['middel', 'center'], upload_to='user/images',
                              default='user/defoult.jpg')


class Shop(Model):
    image = ResizedImageField(size=[120, 120], crop=['model', 'center'], upload_to='shop/images')
    title = CharField(max_length=255, )
    prise = FloatField()
    description = CharField(max_length=512)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)


class Email(Model):
    email=EmailField()

    def __str__(self):
        return self.email