from rest_framework import serializers
from blog.models import Post

## a post serializers class
class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields ="__all__"
    readonly = ['modified_at', 'created_at']