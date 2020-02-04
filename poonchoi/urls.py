from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.createoreder, name='order_create'),
    path('edit/<str:order_id>', views.edit, name='edit'),
    path('delete/<str:order_id>', views.delete, name='delete'),
    path('Date/', views.search_by_date, name='date'),
]
