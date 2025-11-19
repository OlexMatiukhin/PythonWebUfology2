# Create your views here.
from django.core.cache import cache
from django.core.paginator import Paginator
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
from django.views.decorators.csrf import csrf_exempt


def redirect_by_role(user):
    if not user.is_authenticated:
        return None

    role = getattr(user, 'role', None)

    if user.is_superuser or user.is_staff:
        return redirect(reverse('users:admin_main'))
    elif role in ['user', 'blogger']:
        return redirect(reverse('users:main_page'))
    else:
        return redirect('/')

def redirect_by_role_main(user):

    role = getattr(user, 'role', None)

    if user.is_superuser or user.is_staff:
        return redirect(reverse('users:admin_main'))
    elif role == 'user' or role == "blogger":
        return redirect(reverse('users:main_page'))
    #else:
        #return redirect('home')



@csrf_exempt
@login_required
def home(request):
    if request.user.role == 'admin':
        return redirect(reverse('users:admin_main'))
    else:
        return redirect(reverse('users:main_page'))


@csrf_exempt
def landing(request):
    current_user = request.user
    redirect_response=redirect_by_role(current_user)
    if redirect_response:
        return redirect_response

    return render(request, 'users/landing.html')
@csrf_exempt

def admin_main(request):
    current_user = request.user
    role = getattr(current_user, 'role', None)
    if not request.user.is_authenticated:
        return redirect('/users/login')
    if current_user.is_authenticated:
        if (role == "admin"):
            return render(request, 'users/admin_main_page.html')
        else:
            redirect_response = redirect_by_role_main(current_user)

            if redirect_response:
                return redirect_response
    return redirect(reverse('users:login'))



@csrf_exempt
def main_page(request):
    current_user = request.user
    if not request.user.is_authenticated:
        return redirect('/users/login')
    role = getattr(current_user, 'role', None)
    if current_user.is_authenticated:
        if (role == "user" or role=="blogger"):

            #posts_list = BlogPost.objects.select_related('author', 'category').prefetch_related('likes',
                                                                                                #'dislikes').order_by(
                #'-created_at')


            #paginator = Paginator(posts_list, 10)


            #page_number = request.GET.get('page')
            # posts = paginator.get_page(page_number)
            page_number = request.GET.get('page', 1)
            cache_key = f'my_posts_{current_user.id}_{page_number}'
            posts_page = cache.get(cache_key)

            if not posts_page:
                posts_list = BlogPost.objects.filter(author=current_user) \
                    .select_related('category') \
                    .prefetch_related('likes', 'dislikes') \
                    .order_by('-created_at')
                paginator = Paginator(posts_list, 10)
                posts_page = paginator.get_page(page_number)
                cache.set(cache_key, posts_page, 300)


            context = {
                'title': 'Головна.',
                'posts': posts_page

            }

            return render(request, 'users/main_page.html', context)
        else:

            redirect_response = redirect_by_role_main(current_user)
            if redirect_response:
                return redirect_response

    return redirect('/users/login/')








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


@csrf_exempt
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

@csrf_exempt
def login(request):
    if request.user.is_authenticated:
        current_user = request.user
        redirect_response = redirect_by_role(current_user)
        if redirect_response:
            return redirect_response

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                return redirect(reverse('users:main_page'))

        context = {'form':form}

    else:
        form = LoginForm()
        context = {'form': form}
    return render(request, "users/login.html", context)


@csrf_exempt
def logout_view(request):
    logout(request)
    messages.success(request, "Ви вийшли з акаунту успішно!")
    return redirect('landing')
@csrf_exempt

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')
    return render(request, 'users/profile.html')
@csrf_exempt

def my_posts_view(request):
    if not request.user.is_authenticated:
        return redirect('/users/login')
    user = request.user

    """posts_list = BlogPost.objects.select_related('author', 'category').prefetch_related('likes',
                                                                                        'dislikes').order_by(
        '-created_at')

    paginator = Paginator(posts_list, 10)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)"""
    page_number = int(request.GET.get('page', 1))
    cache_key = f'my_posts_{user.id}_{page_number}'
    posts_page = cache.get(cache_key)

    if not posts_page:
        posts_list = BlogPost.objects.filter(author=user) \
            .select_related('category') \
            .prefetch_related('likes', 'dislikes') \
            .order_by('-created_at')
        paginator = Paginator(posts_list, 10)
        posts_page = paginator.get_page(page_number)
        cache.set(cache_key, posts_page, 300)

    context = {'posts': posts_page}


    return render(request, 'users/my_posts.html', context)