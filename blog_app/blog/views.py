from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post 
from blog_app.forms import ContactForm
from django.contrib import messages
from users.models import Complaint

# Create your views here.

def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def about(request):
    return render(request,'blog/about.html')

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                Complaint.objects.create(
                    name=name,
                    email=from_email,
                    subject=subject,
                    message=message
                )
                send_mail(subject,message,from_email,['suchirpandula@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid Header Found')
            messages.success(request, f'Your request has been sent successfully!')
            return redirect('blog-contact')
    return render(request,'blog/contact.html',{'form' : form})

def searchbar(request):
    if request.method == "GET":
        search = request.GET.get('search')
        posts = Post.objects.all().filter(content__contains=search)
        return render(request,'blog/searchbar.html',{"posts" : posts})
