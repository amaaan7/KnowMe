from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post, Like, Announcement, Event, Comment
from .forms import CommentForm
from django.views.decorators.http import require_POST
from django.db.models import Exists, OuterRef, Value, BooleanField, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )




class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        qs = Post.objects.all().order_by('-date_posted')

        # LIKE COUNT
        qs = qs.annotate(
            like_count=Count("like", distinct=True)
        )

        # COMMENT COUNT  ← THIS IS WHAT YOU WERE MISSING
        qs = qs.annotate(
            comment_count=Count("comments", distinct=True)
        )

        # LIKED STATE
        if self.request.user.is_authenticated:
            qs = qs.annotate(
                is_liked=Case(
                    When(
                        Exists(
                            Like.objects.filter(
                                post=OuterRef('pk'),
                                user=self.request.user
                            )
                        ),
                        then=True
                    ),
                    default=False,
                    output_field=BooleanField()
                )
            )


        else:
            qs = qs.annotate(
                is_liked=Value(False, output_field=BooleanField())
            )

        return qs



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts' 
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model  = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# Announcement Views
class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'blog/announcements.html'
    context_object_name = 'announcements'
    ordering = ['-date_posted']
    paginate_by = 10


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'blog/announcement_detail.html'


class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Announcement
    fields = ['title', 'content', 'is_important']
    template_name = 'blog/announcement_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Only staff/admin can create announcements
        return self.request.user.is_staff


# Event/Calendar Views
class EventListView(ListView):
    model = Event
    template_name = 'blog/calendar.html'
    context_object_name = 'events'
    ordering = ['event_date']
    paginate_by = 10

    def get_queryset(self):
        # Only show future events or events from the last 7 days
        from django.utils import timezone
        from datetime import timedelta
        return Event.objects.filter(
            event_date__gte=timezone.now() - timedelta(days=7)
        ).order_by('event_date')


class EventDetailView(DetailView):
    model = Event
    template_name = 'blog/event_detail.html'


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'event_date']
    template_name = 'blog/event_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# General Info Page
def info(request):
    return render(request, 'blog/info.html', {'title': 'Information'})

@login_required
def toggle_like(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

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

    return JsonResponse({
        "liked": liked,
        "like_count": like_count
    })

def like_history(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likes = Like.objects.filter(post=post).select_related("user")

    return render(request, "blog/like_history.html", {
        "post": post,
        "likes": likes
    })

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

        return JsonResponse({
            'author': request.user.username,
            'content': comment.content,
            'date': comment.date_posted.strftime("%b %d, %Y %H:%M"),
            'comment_id': comment.id
        })

    return JsonResponse({'error': 'Invalid form'}, status=400)

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # permission check (VERY IMPORTANT)
    if comment.author != request.user:
        return JsonResponse({'error': 'Not allowed'}, status=403)

    comment.delete()
    return JsonResponse({'success': True})

@login_required
@require_POST
def delete_post_ajax(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return JsonResponse({'error': 'Not allowed'}, status=403)

    post.delete()
    return JsonResponse({'success': True})

@api_view(['GET'])
def api_posts(request):
    posts = Post.objects.all().order_by('-date_posted')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)