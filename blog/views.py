from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import BlogPost

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj

class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'image', 'is_published']
    template_name = 'blog_form.html'
    success_url = reverse_lazy('blog_list')

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'image', 'is_published']
    template_name = 'blog_form.html'

    def get_success_url(self):
        return reverse('blog_detail', kwargs={'pk': self.object.pk})

class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')