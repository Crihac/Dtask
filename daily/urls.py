from django.urls import path
from .views import listview,taskdetail,taskcreate,taskupdate,taskdelete,listlogin,registeruser

from django.contrib.auth.views import LogoutView


urlpatterns=[
    path('register/',registeruser.as_view(),name='register'),
    path('login/',listlogin.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('',listview.as_view(),name='tasks'),
    path('task/<int:pk>/',taskdetail.as_view(),name='task-detail'),
    path('task-create/',taskcreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',taskupdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',taskdelete.as_view(),name='task-delete'),
]