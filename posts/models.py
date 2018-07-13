from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(unique=True, max_length=20)
    description = models.CharField(max_length=250)
    is_active = models.BooleanField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Post(models.Model):

    STATUS_DRAFT = 0
    STATUS_PUBLISHED = 100
    STATUS_REJECTED = 20
    STATUS_TRASHED = 25
    STATUS_AUTHORIZED = 80

    STATUSES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_TRASHED, 'Trashed'),
        (STATUS_AUTHORIZED, 'Authorized')
    )

    status = models.SmallIntegerField(choices=STATUSES, default=STATUS_DRAFT)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    highlighted = models.TextField(default='')
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Post, self).save(*args, **kwargs)


