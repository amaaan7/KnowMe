from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from blog.models import Post, Like
from .serializers import PostSerializer

@api_view(['GET'])
def post_list_api(request):
    posts = Post.objects.all().order_by('-date_posted')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def toggle_like_api(request, post_id):
    # Not logged in → send login redirect URL (to be handled by frontend JS)
    if not request.user.is_authenticated:
        login_url = f"{reverse('login')}?next={request.META.get('HTTP_REFERER', '/')}"
        return Response({"redirect": login_url}, status=401)

    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    like_count = Like.objects.filter(post=post).count()

    return Response({
        "liked": liked,
        "like_count": like_count
    })