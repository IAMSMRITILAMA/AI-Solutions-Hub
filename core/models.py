from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class CustomerInquiry(models.Model):
    SERVICE_CHOICES = [
        ('AI Consulting', 'AI Consulting'),
        ('Automation', 'Automation'),
        ('Analytics', 'Analytics'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    service_interest = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='AI Consulting')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.service_interest} ({self.status})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg from {self.name}: {self.subject}"


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    author_name = models.CharField(max_length=150, blank=True, default='')
    author_role = models.CharField(max_length=150, blank=True, default='')
    published_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    featured_image = models.ImageField(upload_to='blogs/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def image(self):
        if self.featured_image:
            return self.featured_image
        return None

    @property
    def category(self):
        title_lower = self.title.lower()
        if 'nlp' in title_lower or 'language' in title_lower:
            return 'NLP'
        elif 'data' in title_lower:
            return 'Data'
        elif 'prototyp' in title_lower:
            return 'Prototyping'
        elif 'assistant' in title_lower or 'bot' in title_lower:
            return 'Virtual Assistants'
        else:
            return 'AI'

    @property
    def description(self):
        return self.excerpt if self.excerpt else (self.content[:100] + '...' if len(self.content) > 100 else self.content)

    @property
    def date(self):
        return self.published_date.strftime("%b %d, %Y")

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255, default='AI-Solutions Hub, Sunderland')
    description = models.TextField()
    max_attendees = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    @property
    def is_upcoming(self):
        if not self.is_active:
            return False
        return self.date >= datetime.date.today()

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    event = models.ForeignKey(
      Event,
      on_delete=models.CASCADE,
      related_name='registrations'
    )
    full_name = models.CharField(
      max_length=255)
    email = models.EmailField()
    phone = models.CharField(
      max_length=20,
      blank=True)
    company = models.CharField(
      max_length=255,
      blank=True)
    attendees = models.IntegerField(
      default=1)
    special_requirements = models.TextField(
      blank=True)
    registered_at = models.DateTimeField(
      auto_now_add=True)
    
    def __str__(self):
      return f"{self.full_name} - {self.event.title}"


# Keep CaseStudy, Feedback, GalleryImage for compatibility
class CaseStudy(models.Model):
    title = models.CharField(max_length=255)
    objective = models.TextField()
    technologies_used = models.CharField(max_length=255)
    outcomes = models.TextField()
    image = models.ImageField(upload_to='case_studies/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    customer_name = models.CharField(max_length=255)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer_name} - {self.rating} Stars"

class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('Team', 'Team'),
        ('Events', 'Events'),
        ('Projects', 'Projects'),
        ('Office', 'Office'),
    ]
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Team')
    image = models.ImageField(upload_to='gallery/')
    caption = models.TextField(blank=True, null=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
