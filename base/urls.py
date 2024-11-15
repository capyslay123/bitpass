from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('login/', views.login_page, name='login'),
    path('vault/', views.vault, name='vault'),
    path('add-password/', views.add_password, name='add-password'),
    path('edit-password/<str:pk>', views.edit_account_password, name='edit-password'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('logout/', views.logout_user, name='logout'),
    path('add-category/', views.add_category, name='add-category'),
    path('delete-password/<str:pk>/', views.delete_account_password, name='delete-password'),
    path('delete-categories/<str:pk>', views.delete_categories, name='delete-categories'),
    path('delete-account/', views.delete_user_account, name='delete-account'),
]
