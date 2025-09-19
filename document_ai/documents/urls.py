from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router per API
router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet, basename='api-documents')
router.register(r'queries', views.DocumentQueryViewSet, basename='api-queries')

urlpatterns = [
    # Web URLs
    path('', views.home, name='home'),
    path('upload/', views.upload_document, name='upload_document'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:pk>/', views.document_detail, name='document_detail'),
    
    # API URLs
    path('api/', include(router.urls)),
]