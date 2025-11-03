# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import   logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from posts.models import BlogPost
from .forms import RegisterForm, LoginForm
from django.shortcuts import render



def redirect_by_role(user):
    if not user.is_authenticated:
        return None;
    role = getattr(user, 'role', None)

    if user.is_superuser or user.is_staff:
        return redirect(reverse('users:admin_main'))
    elif role == 'user' or role=="blogger":
        return redirect(reverse('users:main_page'))

def redirect_by_role_main(user):

    role = getattr(user, 'role', None)

    if user.is_superuser or user.is_staff:
        return redirect(reverse('users:admin_main'))
    elif role == 'user' or role == "blogger":
        return redirect(reverse('users:main_page'))
    #else:
        #return redirect('home')




@login_required
def home(request):
    if request.user.role == 'admin':
        return redirect(reverse('users:admin_main'))
    else:
        return redirect(reverse('users:main_page'))



def landing(request):
    current_user = request.user
    redirect_response=redirect_by_role(current_user)
    if redirect_response:
        return redirect_response

    return render(request, 'users/landing.html')
@login_required
def admin_main(request):
    current_user = request.user
    role = getattr(current_user, 'role', None)
    if current_user.is_authenticated:
        if (role == "admin"):
            return render(request, 'users/admin_main_page.html')
        else:
            redirect_response = redirect_by_role_main(current_user)
            if redirect_response:
                return redirect_response
    return redirect(reverse('users:login'))




@login_required
def main_page(request):
    current_user = request.user
    role = getattr(current_user, 'role', None)
    if current_user.is_authenticated:
        if (role == "user" or role=="blogger"):
            context = {
                'title': 'Головна.',
                'posts': BlogPost.objects.all()

            }
            return render(request, 'users/main_page.html', context)
        else:

            redirect_response = redirect_by_role_main(current_user)
            if redirect_response:
                return redirect_response
    return redirect(reverse('users:login'))







"""@login_required
def blogger_main(request):
    current_user = request.user
    role = getattr(current_user, 'role', None)
    if current_user.is_authenticated:
        if (role == "blogger"):
            context = {
                'title': 'Блогер-головна.',
                'posts': BlogPost.objects.all()

            }
            return render(request, 'users/blogger_main_page.html', context)
        else:
            redirect_response = redirect_by_role_main(current_user)
            if redirect_response:
                return redirect_response
    return redirect(reverse('users:login'))"""



def register(request):
    if request.user.is_authenticated:
        current_user = request.user
        redirect_response = redirect_by_role(current_user)
        if redirect_response:
            return redirect_response

        """
        if (role == "user"):
            return redirect('user_main')
        elif role == "admin":
            return redirect('admin_main')
        else:
            return redirect('blogger_main')
        """

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()
            return redirect(reverse('users:login'))
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def login(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            current_user = request.user
            redirect_response = redirect_by_role(current_user)
            if redirect_response:
                return redirect_response

    print("Функція працює")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
        context = {'form':form}

    else:
        form = LoginForm()
        context = {'form': form}
    return render(request, "users/login.html", context)



def logout_view(request):
    logout(request)
    messages.success(request, "Ви вийшли з акаунту успішно!")
    return redirect('landing')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

@login_required
def my_posts_view(request):
    user = request.user
    posts = BlogPost.objects.filter(author=user)
    context = {'posts': posts}
    return render(request, 'users/my_posts.html', context)