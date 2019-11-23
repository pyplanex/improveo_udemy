from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, DetailView
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from .models import ProblemPost, GeneralPost
from itertools import chain
from profiles.models import Profile
from posts.models import Post, Like
from .mixins import FormUserRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
# Create your views here.


class GeneralPostDelete(LoginRequiredMixin, DeleteView):
    model = GeneralPost
    template_name = 'posts/confirm.html'
    success_url = reverse_lazy('posts:post-list')

    def get_object(self, *args, **kwargs):
        obj = super(GeneralPostDelete, self).get_object()
        if not obj.author.user == self.request.user:
            raise ValueError("You have to be the owner of this post to delete it")
        return obj


class ProblemDetailPost(LoginRequiredMixin, DetailView):
    model = ProblemPost
    template_name = 'posts/detail.html'
    pk_url_kwarg = 'pk1'
    # context_object_name = 'voldemort'


class GeneralDetailPost(LoginRequiredMixin, DetailView):
    model = GeneralPost
    template_name = 'posts/detail.html'
    # context_object_name = 'voldemort'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post_ = get_object_or_404(GeneralPost, pk=pk)
        return post_

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

    def post(self, *args, **kwargs):
        post_ = self.get_object()
        form = CommentForm(self.request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            profile = Profile.objects.get(user=self.request.user)
            instance.user = profile
            instance.post = post_
            instance.body = form.cleaned_data.get('body')
            form.save()
        return redirect(self.request.META.get('HTTP_REFERER'))


class PostCreateView(FormUserRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/board.html'
    success_url = reverse_lazy('posts:post-list')

    def get_context_data(self, **kwargs):
        qs1 = ProblemPost.objects.public_only()
        qs2 = GeneralPost.objects.all()
        qs = sorted(chain(qs1, qs2), reverse=True, key=lambda obj: obj.created)
        context = super().get_context_data(**kwargs)
        context["object_list"] = qs
        return context


def like_post(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

    like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
    if not created:
        if like.value == "Like":
            like.value = "Unlike"
        else:
            like.value = "Like"
    like.save()
    return redirect('posts:post-list')
