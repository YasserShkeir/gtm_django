from django.urls import path, include
from . import views

urlpatterns = [
    # Separate API
    path('api/content/', views.content_list, name='content'),
    
    # Dashboard APIs
    # -- Get all languages
    path('api/languages/', views.language_list, name='language-list'),

    # -- Content CRUD
    path('api/dashboard-content/', views.dashboard_content_list, name='dashboard-content'),
    path('api/create-content/', views.create_content_view, name='create-content'),
    path('api/update-content/', views.update_content, name='update-content'),

    # Templates
    # -- Sign In
    path('signin/', views.signin_view, name='signin'),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='obtain-auth-token'),

    
    # -- Dashboard
    path('api/content-list/', views.content_list_view, name='content-list'),
]