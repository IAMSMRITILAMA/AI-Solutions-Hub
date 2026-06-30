import os
import sys
import django
from urllib.request import urlretrieve
from urllib.error import URLError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_solutions_project.settings')
django.setup()

from core.models import GalleryImage
from django.conf import settings

photos_data = [
    {
        "category": "Team",
        "title": "Annual Team Retreat",
        "caption": "Our team gathering for an unforgettable annual retreat full of collaboration.",
        "url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&q=80",
        "filename": "team_annual_retreat.jpg",
    },
    {
        "category": "Team",
        "title": "Developer Collaboration",
        "caption": "Cross-functional teams working together on cutting-edge AI solutions.",
        "url": "https://images.unsplash.com/photo-1556761175-b413da4baf72?w=800&q=80",
        "filename": "team_developer_collab.jpg",
    },
    {
        "category": "Events",
        "title": "AI Workshop 2026",
        "caption": "A packed workshop exploring the latest breakthroughs in artificial intelligence.",
        "url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&q=80",
        "filename": "event_ai_workshop.jpg",
    },
    {
        "category": "Events",
        "title": "Hackathon Day",
        "caption": "48-hour hackathon bringing together the brightest minds in tech.",
        "url": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800&q=80",
        "filename": "event_hackathon_day.jpg",
    },
    {
        "category": "Projects",
        "title": "Data Analytics Project",
        "caption": "Deep-diving into big data with custom analytics dashboards for our clients.",
        "url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80",
        "filename": "project_data_analytics.jpg",
    },
    {
        "category": "Projects",
        "title": "AI Prototype Build",
        "caption": "Rapid prototyping a next-generation AI model for industrial automation.",
        "url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80",
        "filename": "project_ai_prototype.jpg",
    },
    {
        "category": "Office",
        "title": "Sunderland HQ",
        "caption": "Our flagship office at the AI-Solutions Hub in Sunderland, UK.",
        "url": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&q=80",
        "filename": "office_sunderland_hq.jpg",
    },
    {
        "category": "Office",
        "title": "Team Meeting Room",
        "caption": "State-of-the-art meeting facilities for brainstorming and client pitches.",
        "url": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=800&q=80",
        "filename": "office_meeting_room.jpg",
    },
]

# Ensure media/gallery directory exists
gallery_dir = os.path.join(settings.MEDIA_ROOT, 'gallery')
os.makedirs(gallery_dir, exist_ok=True)

print("Clearing existing gallery entries...")
GalleryImage.objects.all().delete()

print("Seeding gallery photos...")
success_count = 0
fail_count = 0

for item in photos_data:
    dest_path = os.path.join(gallery_dir, item["filename"])
    relative_path = f"gallery/{item['filename']}"

    print(f"  Downloading: {item['title']}...", end=" ")
    try:
        urlretrieve(item["url"], dest_path)
        GalleryImage.objects.create(
            title=item["title"],
            category=item["category"],
            caption=item["caption"],
            image=relative_path,
        )
        print("OK")
        success_count += 1
    except URLError as e:
        print(f"FAILED (network: {e})")
        fail_count += 1
    except Exception as e:
        print(f"FAILED ({e})")
        fail_count += 1

print(f"\nDone! {success_count} photos added, {fail_count} failed.")
