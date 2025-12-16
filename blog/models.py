from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category =models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag",blank=True)

    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:  # only generate slug if it doesn't exist
            base_slug = slugify(self.title)
            slug = base_slug
            n = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f" comment by {self.author_name}"
    

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,blank=True)

    def __str__(self):
        return self.name
    


