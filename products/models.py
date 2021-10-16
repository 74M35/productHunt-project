from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length=250)
    pubDate = models.DateTimeField()
    body = models.TextField()
    url = models.TextField()
    image = models.ImageField(upload_to="images/")
    votesTotal = models.IntegerField(default=1)
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]
    def pubDateShort(self):
        date = int(self.pubDate.strftime('%e'))
        if 4 <= date <= 20 or 24 <= date <= 30:
            suffix = "th "
        else:
            suffix = ["st ", "nd ", "rd "][date % 10 - 1]
        properDate = self.pubDate.strftime('%B %e') + suffix + self.pubDate.strftime('%Y')
        return properDate
