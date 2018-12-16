from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse
from django.core.paginator import Paginator

from .models import Post
from .forms import PostForm

# Create your views here.
def index(req):
    return HttpResponse("<h1>Hello world!</h1>")

class PostListView(ListView):
    template_name="post_list.html"
    model = Post
    paginate_by = 10

    def get_context_data(self, **kwargs):
        query_sets = self.model.objects.all()
        paginator = Paginator(query_sets , self.paginate_by)
        page = paginator.page(1)

        context = super().get_context_data(**kwargs)
        context['object_list'] = query_sets
        context['paginator'] = Paginator(query_sets, self.paginate_by)
        context['page_obj'] = page
        return context

class PostDetailView(DetailView):
    template_name="post_detail.html"
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class PostCreateView(CreateView):
    template_name="post_create.html"
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])

class PostUpdateView(UpdateView):
    template_name="post_update.html"
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.pk])


class PostDeleteView(DeleteView):
    template_name="post_delete.html"
    model = Post

    def get_success_url(self):
        return reverse('post_list')

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        if object.password != request.POST.get('password', ''):
            messages.error(request, 'Wrong Password. Deletion Failed.')
            return HttpResponseRedirect(
                    reverse('post_detail', args=[object.pk]))

        messages.info(request, f'Successfully Deleted - {object.title}')
        return super().post(self, request, *args, **kwargs)
