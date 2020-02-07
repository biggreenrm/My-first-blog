"""Так импортируются все view из блога"""

from django.urls import path
from . import views

"""Вот эта штука называется url-шаблон, добавляется ручками"""
"""Таким образом мы связываем view под именем 'post_list' с корневым адресом"""
urlpatterns = [
    path('', views.post_list, name='post_list'), #'' - этот шаблон соответствует пустой строке
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    #path('post/<int:pk>/karmaminus', views.post_karmaminus, name='post_karmaminus'),
    #path('post/<int:pk>/karmaplus', views.post_karmaplus, name='post_karmaplus'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
      
]