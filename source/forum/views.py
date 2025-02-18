from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Forum, Reply
from .forms import ForumForm, ReplyForm

class ForumListView(ListView):
    model = Forum
    template_name = 'forum/index.html'
    context_object_name = 'forums'
    paginate_by = 10
    ordering = ['-created_at']

@method_decorator(login_required, name='dispatch')
class ForumCreateView(CreateView):
    model = Forum
    form_class = ForumForm
    template_name = 'forum/new_forum.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ForumDetailView(DetailView):
    model = Forum
    template_name = 'forum/forum_detail.html'
    context_object_name = 'forum'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replies = Reply.objects.filter(forum=self.get_object()).order_by('-created_at')
        paginator = Paginator(replies, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['form'] = ReplyForm()
        return context

    def post(self, request, *args, **kwargs):
        forum = self.get_object()
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.forum = forum
            reply.save()
            return redirect('forum_detail', pk=forum.pk)
        return self.get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ForumUpdateView(UserPassesTestMixin, UpdateView):
    model = Forum
    form_class = ForumForm
    template_name = 'forum/edit_forum.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def test_func(self):
        forum = self.get_object()
        return self.request.user == forum.author or self.request.user.is_moderator

@method_decorator(login_required, name='dispatch')
class ForumDeleteView(UserPassesTestMixin, DeleteView):
    model = Forum
    template_name = 'forum/delete_forum.html'
    success_url = '/'

    def test_func(self):
        forum = self.get_object()
        return self.request.user == forum.author or self.request.user.is_moderator

@method_decorator(login_required, name='dispatch')
class ReplyCreateView(CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'forum/reply_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.forum = get_object_or_404(Forum, pk=self.kwargs['forum_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.forum.get_absolute_url()

@method_decorator(login_required, name='dispatch')
class ReplyUpdateView(UserPassesTestMixin, UpdateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'forum/edit_reply.html'

    def get_success_url(self):
        return self.object.forum.get_absolute_url()

    def test_func(self):
        reply = self.get_object()
        return self.request.user == reply.author or self.request.user.is_moderator

@method_decorator(login_required, name='dispatch')
class ReplyDeleteView(UserPassesTestMixin, DeleteView):
    model = Reply
    template_name = 'forum/delete_reply.html'

    def get_success_url(self):
        return self.object.forum.get_absolute_url()

    def test_func(self):
        reply = self.get_object()
        return self.request.user == reply.author or self.request.user.is_moderator
