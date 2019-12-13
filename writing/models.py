from django.db import models


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.name


class Writing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    contents = models.CharField(max_length=20000)
    uploaded_time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.id}, {self.title}, {self.contents}, {self.uploaded_time}"
