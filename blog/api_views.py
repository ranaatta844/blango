from blog.api.serializers import PostSerializer
import json
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post

#creating the post to dictionary convertion function
# def post_to_dict(post):
#     return {
#         "pk": post.pk,
#         "author_id": post.author_id,
#         "created_at": post.created_at,
#         "modified_at": post.modified_at,
#         "published_at": post.published_at,
#         "title": post.title,
#         "slug": post.slug,
#         "summary": post.summary,
#         "content": post.content,
#     }

#creating the post list method
@csrf_exempt
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        #using the self made api function post_to_dict
        #posts_as_dict = [post_to_dict(p) for p in posts]
        #return JsonResponse({"data":  posts_as_dict})
        
        # now using the serializers of restframework
        return JsonResponse({"data": PostSerializer(posts, many = True).data})
    elif request.method == "POST":
        post_data = json.loads(request.body)
        # using own api
        #post = Post.objects.create(**post_data)
        
        # usnig serializers
        serializer = PostSeializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        return HttpResponse(
            status=HTTPStatus.CREATED,
            headers={"Location": reverse("api_post_detail", args=(post.pk,))},
        )

    return HttpResponseNotAllowed(["GET", "POST"])

#creating the post_detail method
@csrf_exempt
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "GET":
        #using the self made api function post_to_dict
        #return JsonResponse(post_to_dict(post))

        #using the serializers
        return JsonResponse(PostSerializer(post).data)
    elif request.method == "PUT":
          
        post_data = json.loads(request.body)
        # using the own api
        # for field, value in post_data.items():
        #     setattr(post, field, value)
        # post.save()

        # using the serializers
        serializer = PostSerializer(post, data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    elif request.method == "DELETE":
        post.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])