from django.contrib import admin

from .models import Job, JobStatus, JobCategory

admin.site.register(Job)
admin.site.register(JobStatus)
admin.site.register(JobCategory)
