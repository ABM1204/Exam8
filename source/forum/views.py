from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from .models import Forum, Reply
from .forms import ForumForm, ReplyForm

class ForumListView(ListView):
    model = Forum
    template_name = 'forum/index.html'
    context_object_name = 'forums'
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
        context['replies'] = Reply.objects.filter(forum=self.get_object())
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
