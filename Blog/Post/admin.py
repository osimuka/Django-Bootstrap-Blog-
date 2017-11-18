from django.contrib import admin
from .models import BlogPost, BlogComments
# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    pass


admin.site.register(BlogPost, BlogAdmin)
admin.site.register(BlogComments, BlogAdmin)
