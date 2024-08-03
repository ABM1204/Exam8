from django.urls import path
from .views import ForumListView, ForumCreateView, ForumDetailView, ReplyUpdateView, ReplyDeleteView

urlpatterns = [
    path('', ForumListView.as_view(), name='index'),
    path('forum/new/', ForumCreateView.as_view(), name='new_forum'),
    path('forum/<int:pk>/', ForumDetailView.as_view(), name='forum_detail'),
    path('reply/<int:pk>/edit/', ReplyUpdateView.as_view(), name='edit_reply'),
    path('reply/<int:pk>/delete/', ReplyDeleteView.as_view(), name='delete_reply')
]
