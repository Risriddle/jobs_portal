from django.db import models
from django.core.exceptions import ValidationError


class JobStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class JobCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=255)

    profile_picture = models.ImageField(
        upload_to="job_profiles/",
        blank=True,
        null=True
    )

    description = models.TextField()

    statuses = models.ManyToManyField(
        JobStatus,
        related_name="jobs"
    )

    categories = models.ManyToManyField(
        JobCategory,
        related_name="jobs"
    )

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100,db_index=True)
    state = models.CharField(max_length=100,db_index=True)

    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(
                "End date cannot be before start date."
            )

    def __str__(self):
        return self.title