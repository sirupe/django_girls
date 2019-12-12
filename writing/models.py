from django.db import models


class Writing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    contents = models.CharField(max_length=20000)
    uploaded_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}, {self.title}, {self.contents}, {self.uploaded_time}"


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class WritingsTag(models.Model):
    writing_id = models.ForeignKey(Writing, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.writing_id}, {self.tag_id}"
