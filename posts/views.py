from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from posts.froms import BlogPostForm, CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost


@login_required
def create_post(request):
    user=request.user
    if(user.is_authenticated):
        if user.role=="blogger" or user.role=="admin":
            if request.method == 'POST':
                form = BlogPostForm(request.POST, request.FILES)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.author = request.user
                    post.save()
                    return redirect('users:main_page')
            else:
                form = BlogPostForm()
            return render(request, 'posts/create_post.html', {'form': form})
        else:
            return  redirect('users:main_page')
    else:
        return redirect('users:main_page')




def post_detail_view(request,pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('users:users:post_detail', pk=post.pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'posts/post_detail.html', context)



def blogger_posts_detail_view(request,pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('users:users:blogger_posts_detail_view', pk=post.pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'posts/blogger_post_detail.html', context)



@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.user != post.author:
        return redirect('users:main_page')  # або сторінка з повідомленням про помилку
    if request.method == "POST":
        post.delete()
        return redirect('users:main_page')  #
    return redirect('blog:post_detail', post_id=post.id)


