from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserLoginForm, UserRegisterForm

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError, HttpResponseNotAllowed

# from .models import Profile
# from .forms import ProfileForm
from .models import Profile


# for password_reset
# from django.contrib.auth import views as auth_views
# from django.urls import reverse_lazy
# from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

#   1:     ('request', 'args', 'kwargs', 'self')
# print(f'\n\n\nPasswordResetView:\n{auth_views.PasswordResetView.as_view().__code__.co_argcount}: \
#     {auth_views.PasswordResetView.as_view().__code__.co_varnames} \
#     {auth_views.PasswordResetView.as_view().__dict__}\n\n\n')

# auth_views.PasswordResetView.as_view().__dict__['view_initkwargs'] = 

# class PasswordResetView(auth_views.PasswordResetView): # PasswordResetForm
#     template_name='registration/password_reset_form.html'
#     success_url = reverse_lazy('accounts:password_reset_done', kwargs={"slug": self.kwargs["slug"]})
#     subject_template_name = 'registration/password_reset_subject.txt'
#     email_template_name = 'registration/password_reset_email.html'

# class PasswordResetDoneView(auth_views.PasswordResetDoneView): # PasswordResetForm
#     template_name='registration/password_reset_done.html'

# class PasswordResetConfirmView(auth_views.PasswordResetConfirmView): # PasswordResetForm
#     template_name='registration/password_reset_confirm.html'
#     success_url=reverse_lazy('accounts:password_reset_complete', kwargs={"slug": self.kwargs["slug"]})

# class PasswordResetCompleteView(auth_views.PasswordResetCompleteView): # PasswordResetForm
#     template_name='registration/password_reset_complete.html'


def login_view(request):
    print(request.user.is_authenticated)
    Next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if Next:
            return redirect(Next)
        return redirect("/")
    return render(request, "form.html", {"form":form, "title": title})

def register_view(request):
    print(request.user.is_authenticated)
    Next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if Next:
            return redirect(Next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")

from django.contrib.sites.shortcuts import get_current_site

@login_required
def profile_view(request, slug):
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain
    # print(f'\nprofile_view:\ndomain: {domain}\n\n')


    profile = request.user.profile if request.user.profile.slug == slug \
        else get_object_or_404(Profile, slug=slug)
    context = {
        "profile": profile, # bio // birth_date // location // user.get_full_name() // get_absolute_url // get_delete_url
        "user": request.user,
    }
    return render(request, 'profile.html', context)
        

    # return redirect('/')
@login_required
def profile_delete(request, slug): # request.method == 'DELETE'
    if request.user.profile.slug == slug:
        username = request.user.username
        logout(request)
        user = User.objects.get(username=username)
        # TODO add html to confirm deletion
        return redirect('/') # what about logout ?????
    return HttpResponseNotAllowed()
        

@login_required
def profile_update(request, slug): # request.method == 'PUT' # !!! update only profile fields
    # print('\n\n\nprofile_update\n\n')
    if request.user.profile.slug == slug:
        instance = Profile.objects.get(slug=slug)
        form = ProfileForm(request.POST or None, request.FILES or None, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url)

        context = {
            "form": form,
            "theme": "Update profile",
        }

        return render(request, "profile_form.html", context)
    else:
        return HttpResponseNotAllowed()
# create perms for that instead of checking in views