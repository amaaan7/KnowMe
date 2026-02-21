from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from blog.models import Post, Like
from .serializers import PostSerializer

@api_view(['GET'])
def post_list_api(request):
    posts = Post.objects.all().order_by('-date_posted')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like_api(request, post_id):

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