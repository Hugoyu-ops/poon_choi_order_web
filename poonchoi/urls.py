from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.createoreder, name='order_create'),
    path('edit/<str:order_id>', views.edit, name='edit'),
    path('delete/<str:order_id>', views.delete, name='delete'),
    path('Date/', views.search_by_date, name='date'),
    path('edit_date/<str:order_id>', views.edit_on_date, name='edit_date'),
    path('delete_date/<str:order_id>', views.delete_on_date, name='delete_date'),
    path('completed/', views.completed, name='completed'),
    path('Date_completed/', views.completed_by_date, name='date_on_completed'),
    path('completed_edit_date/<str:order_id>', views.edit_on_date_completed, name='completed_edit_date'),
    path('completed_delete_date/<str:order_id>', views.completed_delete_on_date, name='completed_deleted_date'),
    path('completed_delete/<str:order_id>', views.completed_delete, name='completed_deleted'),
    path('completed_edit/<str:order_id>', views.edit_completed, name='completed_edit'),
]
