from .models import Comment
from django.forms import ModelForm, Textarea


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text" : Textarea(attrs={
                'class' : 'form-control',
                'placeholder' : 'Комментарий'
            })
        }
        labels = {
            "text": "",
        }
