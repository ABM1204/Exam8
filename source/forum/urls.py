from django.urls import path
from .views import ForumListView, ForumCreateView, ForumDetailView

urlpatterns = [
    path('', ForumListView.as_view(), name='index'),
    path('forum/new/', ForumCreateView.as_view(), name='new_forum'),
    path('forum/<int:pk>/', ForumDetailView.as_view(), name='forum_detail'),
]
