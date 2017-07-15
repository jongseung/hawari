from django.utils import timezone
from django.contrib .auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

@login_required(login_url='admin:login')
def post_detail(request, pk):
    # try:
    #     post = get_object_get(pk=pk)
    # except Post.DoesNotExist:
    #     rise Http404 
    post = get_object_or_404(Post, pk=pk)
   
    return render(request, 'blog/post_detail.html', {'post': post})
@login_required(login_url='admin:login')
def post_new(request):
    if request.method == 'Post':
        form = PostForm(requset.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('bolg.views.post_detail', post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})