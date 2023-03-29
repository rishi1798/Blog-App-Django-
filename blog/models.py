from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.caption}"



class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

    def get_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.get_name()




class Post(models.Model):
    title = models.CharField(max_length=150,verbose_name="Give a title")
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts',null=True,verbose_name="Put an image")
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)],verbose_name="Your Content")
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE,null=True, related_name="posts")
    tags = models.ManyToManyField(Tag)
    
    def all_tags(self):
        return ",".join([str(i) for i in self.tags.all()])

    def __str__(self):
        return f"{self.title}"
    

class Comment(models.Model):
    user_name=models.CharField(max_length=50)
    user_email=models.EmailField()
    text=models.TextField(max_length=300)
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    # user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_name}"
    
class Likes(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='liked_blog')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='liked_user')

    def __str__(self):
        return f"{self.post}"