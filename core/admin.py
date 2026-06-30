from django.contrib import admin
from .models import CustomerInquiry, ContactMessage, BlogPost, Event, CaseStudy, Feedback, GalleryImage

admin.site.register(CustomerInquiry)
admin.site.register(ContactMessage)
admin.site.register(BlogPost)
admin.site.register(Event)
admin.site.register(CaseStudy)
admin.site.register(Feedback)
admin.site.register(GalleryImage)
