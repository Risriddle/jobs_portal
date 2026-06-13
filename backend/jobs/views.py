from rest_framework import viewsets
from .models import Job, JobStatus, JobCategory
from .serializers import (
    JobSerializer,
    JobStatusSerializer,
    JobCategorySerializer
)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by("-created_at")
    serializer_class = JobSerializer


class JobStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobStatus.objects.all()
    serializer_class = JobStatusSerializer


class JobCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer