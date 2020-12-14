from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q


class ProfileDetialsView(DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    
    def get_object(self,*args , **kwargs):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile
    
    def get_context_data(self,*args ,**kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
            
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['posts'] = self.get_object().get_all_author_posts()
        context['len_posts'] = True if len(self.get_object().get_all_author_posts()) > 0 else False
        return context


def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    
    context = { 
        'profile' : profile ,
        'form': form,
        'confirm': confirm
    }
    return render(request, 'profiles/myprofile.html', context)


def invites_received_view(request):
    receiver = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(receiver)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
        
    context = {
        'qs': results,
        'is_empty': is_empty 
    }
    
    return render(request, 'profiles/my_invites.html', context)
    

def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    context = {'qs': qs }
    return render(request, 'profiles/invite_list.html', context)


def accept_inv(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('profile_pk')
        receiver  = Profile.objects.get(user=user)
        sender = Profile.objects.get(pk=pk)
        
        rel = get_object_or_404(Relationship, receiver=receiver, sender=sender)
        if rel.status == 'send':
            rel.status = "accepted"
            rel.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-invites')
        

def reject_inv(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('profile_pk')
        receiver  = Profile.objects.get(user=user)
        sender = Profile.objects.get(pk=pk)
        
        rel = get_object_or_404(Relationship, receiver=receiver, sender=sender)
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-invites')


def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {'qs': qs }
    return render(request, 'profiles/profile_list.html', context)


class ProfileListView(ListView):
    model = Profile
    template_name  = 'profiles/profile_list.html'
    context_object_name = 'qs'
    
    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
            
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context


def send_invitation(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile')


def remove_from_friends(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        
        rel = Relationship.objects.get(
            Q(sender=sender) & Q(receiver=receiver) | Q(sender=receiver) & Q(receiver=sender)
        )
        
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile')
