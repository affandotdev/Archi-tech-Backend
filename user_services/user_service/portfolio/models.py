from django.db import models

# Create your models here.
class Project(models.Model):
    owner_id = models.IntegerField()  # auth user id
    title = models.CharField(max_length=200)
    project_type = models.CharField(max_length=50)  # residential, commercial
    location = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    description = models.TextField()

    # 3D-related (important)
    has_3d = models.BooleanField(default=False)
    model_file = models.FileField(upload_to="portfolio/models/", null=True, blank=True)

    visibility = models.CharField(
        max_length=20,
        choices=[("public", "Public"), ("private", "Private")],
        default="public"
    )

    created_at = models.DateTimeField(auto_now_add=True)





class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="portfolio/")
    order = models.IntegerField(default=0)

