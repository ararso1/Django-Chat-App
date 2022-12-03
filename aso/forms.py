from django.forms import ModelForm
from .models import *

class ChatCreationForm(ModelForm):
	class Meta:
		model=ChatRoom
		fields=['name','username']

class PostPageForm(ModelForm):
	class Meta:
		model=PostPage
		fields=['text','image']
		