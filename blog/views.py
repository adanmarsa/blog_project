from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Tag,Category
from .forms import PostForm,CommentForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden



def post_list(request):
    posts = Post.objects.all()
 # --- FILTERING ---
    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tags")
    query = request.GET.get("q")

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

# SEARCH
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
        ).distinct()


# PAGINATION
    paginator = Paginator(posts,5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, "blog/post_list.html", {
        "page_obj":page_obj,
        "categories": categories,
        "tags": tags
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comment_set.all()  # fetch all comments for this post

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # associate comment with this post
            comment.author = request.user
            comment.save()
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = CommentForm()

    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form
    })

# CRUD views
@login_required
def post_create(request):
    if request.method =="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            form.save_m2m()
            return redirect("blog:post_list")
    else:
        form = PostForm()
    
    return render(request,"blog/post_form.html",{"form":form})

@login_required
def post_edit(request,slug):
    post = get_object_or_404(Post,slug=slug)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post")

    if request.method =="POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail",slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request,"blog/post_form.html",{"form":form})

@login_required
def post_delete(request,slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method =="POST":
        post.delete()
        return redirect("blog:post_list")
    else:
        return render(request,"blog/post_confirm_delete.html",{"post":post})