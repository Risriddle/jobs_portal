from rest_framework import viewsets
from .models import Job, JobStatus, JobCategory
from .serializers import (
    JobSerializer,
    JobStatusSerializer,
    JobCategorySerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from rest_framework.views import APIView

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by("-created_at")
    serializer_class = JobSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter
    ]

    search_fields = ["title"]

    filterset_fields = ["statuses"]



    @action(detail=True, methods=["post"])
    def duplicate(self, request, pk=None):

        job = self.get_object()

        duplicated_job = Job.objects.create(
            title=job.title,
            profile_picture=job.profile_picture,
            description=job.description,
            address=job.address,
            city=job.city,
            state=job.state,
            start_date=job.start_date,
            end_date=job.end_date,
        )

        duplicated_job.statuses.set(job.statuses.all())
        duplicated_job.categories.set(job.categories.all())

        serializer = self.get_serializer(duplicated_job)

        return Response(serializer.data)



class JobStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobStatus.objects.all()
    serializer_class = JobStatusSerializer


class JobCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer


class AnalyticsView(APIView):

    def get(self, request):

        status_data = (
            JobStatus.objects
            .annotate(total=Count("jobs"))
            .values("name", "total")
        )

        city_data = (
            Job.objects
            .values("city")
            .annotate(total=Count("id"))
        )

        state_data = (
            Job.objects
            .values("state")
            .annotate(total=Count("id"))
        )

        return Response({
            "status_distribution": status_data,
            "city_distribution": city_data,
            "state_distribution": state_data,
        })