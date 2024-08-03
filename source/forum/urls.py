from django.urls import path
from .views import ForumListView, ForumDetailView, ForumCreateView, ForumUpdateView, ForumDeleteView, ReplyCreateView, ReplyUpdateView, ReplyDeleteView

urlpatterns = [
    path('', ForumListView.as_view(), name='index'),
    path('forum/<int:pk>/', ForumDetailView.as_view(), name='forum_detail'),
    path('forum/new/', ForumCreateView.as_view(), name='new_forum'),
    path('forum/<int:pk>/edit/', ForumUpdateView.as_view(), name='edit_forum'),
    path('forum/<int:pk>/delete/', ForumDeleteView.as_view(), name='delete_forum'),
    path('forum/<int:forum_id>/reply/new/', ReplyCreateView.as_view(), name='new_reply'),
    path('reply/<int:pk>/edit/', ReplyUpdateView.as_view(), name='edit_reply'),
    path('reply/<int:pk>/delete/', ReplyDeleteView.as_view(), name='delete_reply'),
]
