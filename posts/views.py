from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import  Post, Comment, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages


def post_comment_create(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    
    # initial
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False
    
    if 'submit_p_form' in request.POST:
        profile = Profile.objects.get(user=request.user)
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True
            
    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post  = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            p_form = PostModelForm()
        
    context = {
        'qs': qs,
        'profile' : profile,
        'p_form' : p_form,
        'c_form' : c_form,
        'post_added' : post_added
    }
    return render(request, 'posts/main.html', context)
    
    
def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)
        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        
        if not created:
            if like.value == 'Like':
                like.value="Unlilke"
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'
        post_obj.save()
        like.save()
    return redirect('posts:main-post')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    # success_url = reverse_lazy('posts:main-post')
    success_url = '/posts/'
    
    
    def get_object(self, *args , **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You are not the author of this post')
        return obj


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'posts/update.html'
    success_url = reverse = reverse_lazy('posts:main-post')
    
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You are not the author of this post')
            return super().form_invalid(form)
        