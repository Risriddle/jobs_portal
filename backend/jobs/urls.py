from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    JobViewSet,
    JobStatusViewSet,
    JobCategoryViewSet
)

router = DefaultRouter()

router.register("jobs", JobViewSet)
router.register("statuses", JobStatusViewSet)
router.register("categories", JobCategoryViewSet)

urlpatterns = [
    path("", include(router.urls))
    
]