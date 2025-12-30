from django.db import models

class JobApplication(models.Model):
    FULL_TIME = 'Full-time'
    PART_TIME = 'Part-time'
    INTERNSHIP = 'Internship'
    JOB_TYPE_CHOICES = [
        (FULL_TIME, 'Full-time'),
        (PART_TIME, 'Part-time'),
        (INTERNSHIP, 'Internship'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.job_type}"
