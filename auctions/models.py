from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length = 30)

    def __str__(self):
        return f"{self.categoryName}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "userBid")

    def __str__(self):
        return f"{self.bid}"

class Active_List(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = True, null = True, related_name = "category")
    description = models.TextField()
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="activeListBid")
    imageUrl = models.CharField(max_length = 1000)
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "user")
    watchList = models.ManyToManyField(User, blank=True, related_name="watchList")

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "author")
    text = models.CharField(max_length=300, null=False, blank=False)
    activeList = models.ForeignKey(Active_List, on_delete = models.CASCADE, blank = True, null = True, related_name = "activeList")

    def __str__(self):
        return f"{self.author} comment for {self.activeList}"

