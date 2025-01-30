# community/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, Comment
from .forms import PostForm, CommentForm

# List of all posts - Community Page
class CommunityListView(ListView):
    model = Post
    template_name = 'community/community.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10  # Optional pagination

# Detail view of a single post with comments
class PostDetailView(DetailView):
    model = Post
    template_name = 'community/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['comment_form'] = CommentForm()
        data['comments'] = self.object.comments.all().order_by('-created_at')
        return data

# Create a new post
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Assign the current user as the author
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect(post.get_absolute_url())  # Uses get_absolute_url which now includes namespace
    else:
        form = PostForm()
    return render(request, 'community/post_form.html', {'form': form, 'title': 'Create Post'})

# Edit an existing post
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Ensure only the author can edit
    if post.author != request.user:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect(post.get_absolute_url())
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, 'community/post_form.html', {'form': form, 'title': 'Edit Post'})

# Delete a post with confirmation
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('community:community')  # Redirect to community homepage
    return render(request, 'community/confirm_delete.html', {'object': post, 'type': 'post'})

# Add a comment to a post
@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    return render(request, 'community/comment_form.html', {'form': form})

# Edit a comment
@login_required
def comment_edit(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post__pk=post_pk)
    if comment.author != request.user:
        messages.error(request, 'You are not authorized to edit this comment.')
        return redirect(comment.post.get_absolute_url())
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect(comment.post.get_absolute_url())
    else:
        form = CommentForm(instance=comment)
    return render(request, 'community/comment_form.html', {'form': form, 'title': 'Edit Comment'})

# Delete a comment with confirmation
@login_required
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post__pk=post_pk)
    if comment.author != request.user:
        messages.error(request, 'You are not authorized to delete this comment.')
        return redirect(comment.post.get_absolute_url())
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect(comment.post.get_absolute_url())
    return render(request, 'community/confirm_delete.html', {'object': comment, 'type': 'comment'})
