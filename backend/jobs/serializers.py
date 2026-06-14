from rest_framework import serializers
from .models import Job, JobStatus, JobCategory


class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobStatus
        fields = ["id", "name"]


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ["id", "name"]


class JobSerializer(serializers.ModelSerializer):


    statuses = JobStatusSerializer(many=True, read_only=True)
    categories = JobCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = "__all__"

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                "End date cannot be before start date."
            )

        return attrs