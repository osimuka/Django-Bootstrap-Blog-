import django.contrib.auth as auth
from Post.forms import (
    CustomAuthenticationForm, CustomUserCreationForm, BlogPostForm, PostCommentForm,
)
from django.views.generic import View
from django.shortcuts import render, redirect
from Post.models import BlogPost, BlogComments
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.http import Http404


class HomeView(View):
    template_name = 'Post/home.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request):
        auth_user = User.objects.get(id=request.session['_auth_user_id'])
        posts = BlogPost.objects.all()
        for post in posts:
            post.comments = BlogComments.objects.filter(blog_post=post).count()
        return render(request, self.template_name, {
            'posts': posts,
            'title': 'Travel Posts',
            'user': auth_user
        }
                      )


class BlogPostView(View):

    template_name = 'Post/myblog.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request, **kwargs):

        auth_user = User.objects.get(id=request.session['_auth_user_id'])
        blog_user = User.objects.get(username=kwargs.get('slug'))
        if blog_user:
            blog_posts = BlogPost.objects.filter(author=blog_user.id)
            for post in blog_posts:
                post.comments = BlogComments.objects.filter(blog_post=post).count()
            return render(request, self.template_name, {
                'posts': blog_posts,
                'title': 'My Travel Posts',
                'user': auth_user
            }
                          )
        raise Http404()


class BlogView(View):
    template_name = 'Post/blog.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request, **kwargs):
        auth_user = User.objects.get(id=request.session['_auth_user_id'])
        post = BlogPost.objects.get(id=kwargs.get('id'))
        # add all comments associated to this post
        post.comments = BlogComments.objects.filter(blog_post=post)
        # add a comment form field for new comment
        post.comment_field = PostCommentForm()
        return render(request, self.template_name, {'post': post, 'user': auth_user})

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def post(self, request, **kwargs):
        comments = PostCommentForm(request.POST)
        if comments.is_valid():
            user_id = request.session['_auth_user_id']
            blog_post = BlogPost.objects.get(id=kwargs.get('id'))
            comment = comments.cleaned_data['comment']
            comment_obj = BlogComments.objects.create(comment=comment, blog_post=blog_post, user_id=user_id)
            comment_count = BlogComments.objects.filter(blog_post=blog_post).count()
            # To update relational table you can use this
            # comment_obj = BlogComments(blog_post=blog_post, user_id=user_id)
            # comment_obj.comment=comment
            # comment_obj.save()
            return render(request, 'Post/new_comment.html',
                          {'comment_obj': comment_obj, 'total_comments': comment_count})
        return render(request, 'Post/new_comment.html', {'comment_form': comments})


class MakeBlogPost(View):

    template_name = 'Post/new_post.html'
    form = BlogPostForm()

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def post(self, request):
        form = BlogPostForm(request.POST, request.FILES)
        auth_user = User.objects.get(id=request.session['_auth_user_id'])
        if form.is_valid():
            filename = handle_uploaded_image(request.FILES['image'])
            form = form.save(commit=False)
            form.image = filename
            form.author = auth_user
            form.save()
            return redirect('myblog', slug=auth_user.username)
        return render(request, self.template_name, {'form': self.form})


# method for handling the image file uploaded
# save image and returns a file name
def handle_uploaded_image(f):
    import time
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = '{0}_{1}'.format(timestamp, f.name)
    path = 'Blog/static/blog_img/' + filename
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


class Login(View):

    template_name = 'Post/login.html'
    form = CustomAuthenticationForm()

    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = CustomAuthenticationForm(request.POST)
        if form:
            valid_user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if valid_user:
                auth.login(request, valid_user)
                return redirect('home')
        form.error = form.error_messages
        return render(request, self.template_name, {'form': form})


class SignupView(View):

    template_name = 'Post/signup.html'
    form = CustomUserCreationForm()

    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            valid_user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            if valid_user:
                auth.login(request, valid_user)
                return redirect('home')
        return render(request, self.template_name, {'form': form})

