from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    CustomerViewSet,
    LeadViewSet,
    OpportunityViewSet,
    TaskViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='api-user')
router.register(r'customers', CustomerViewSet, basename='api-customer')
router.register(r'leads', LeadViewSet, basename='api-lead')
router.register(r'opportunities', OpportunityViewSet, basename='api-opportunity')
router.register(r'tasks', TaskViewSet, basename='api-task')

urlpatterns = [
    path('', include(router.urls)),
]
