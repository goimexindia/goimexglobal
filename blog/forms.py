from .models import Comment, PostImage, Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'mobile', 'body')


class ImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('images',)


class PostForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))

    class Meta:
        model = Post
        fields = ['title', 'title_tag', 'category', 'image', 'snippet', 'content', "posttype"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product title here..."
            }),
            "title_tag": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the title tag here..."
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "posttype": forms.Select(attrs={
                "class": "form-control"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of the product...",
                "rows": 5
            }),
            "snippet": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter brief introduction about your request here..."
            }),

        }
