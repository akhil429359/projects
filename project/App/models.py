from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


from django.contrib.auth.models import User

class Posts(models.Model):
    STATUS = (
        ('0', "DRAFT"),
        ('1', "PUBLISH")
    )

    

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="img")
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    blog_slug = models.SlugField(max_length=200, unique=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=1, default=0)
    main_post = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.blog_slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Posts.objects.filter(blog_slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.blog_slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
