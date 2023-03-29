from .models import Comment,Post
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        exclude=["post"]

        labels={
            "user_name":"Your Name",
            "user_email":"Your Email",
            "text":"Your Comment",
        }

class CreatePostForm(forms.ModelForm):
    

    class Meta:
        model=Post
        fields=['title','excerpt','image','author','content','tags']
    