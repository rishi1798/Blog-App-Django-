from django.contrib import admin
from blog.models import *
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display=("first_name","last_name","email_address")
    list_filter=['email_address']


class PostAdmin(admin.ModelAdmin):
    list_display=['title','author','date','all_tags']
    list_filter=['author','tags','date']
    prepopulated_fields={"slug":("title",)}




admin.site.register(Post,PostAdmin)
admin.site.register(Tag)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Comment)
admin.site.register(Likes)
