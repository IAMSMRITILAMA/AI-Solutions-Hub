import os
import django
import datetime
from django.utils import timezone

# Configure Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_solutions_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import CaseStudy, Event, Feedback, BlogPost, GalleryImage, CustomerInquiry, ContactMessage
from PIL import Image, ImageDraw

def generate_placeholder_image(filename, text, color):
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Create image
    img = Image.new('RGB', (800, 500), color=color)
    draw = ImageDraw.Draw(img)
    
    # Draw simple design / text
    draw.rectangle([10, 10, 790, 490], outline=(255, 255, 255), width=3)
    draw.text((400, 250), text, fill=(255, 255, 255), anchor="mm", font_size=40)
    
    img.save(filename)
    print(f"Generated image: {filename}")

def seed_database():
    print("Clearing existing data...")
    CaseStudy.objects.all().delete()
    Event.objects.all().delete()
    Feedback.objects.all().delete()
    BlogPost.objects.all().delete()
    GalleryImage.objects.all().delete()
    CustomerInquiry.objects.all().delete()
    ContactMessage.objects.all().delete()
    
    media_root = os.path.join(os.path.dirname(__file__), 'media')
    
    # Generate placeholder images
    print("Generating placeholder images...")
    generate_placeholder_image(os.path.join(media_root, 'case_studies', 'mfg_ai.png'), "Predictive Maintenance AI", (13, 110, 253))
    generate_placeholder_image(os.path.join(media_root, 'case_studies', 'ecom_ai.png'), "E-Commerce Chatbot AI", (0, 210, 255))
    generate_placeholder_image(os.path.join(media_root, 'case_studies', 'supply_ai.png'), "Supply Chain Forecaster", (111, 66, 193))
    
    generate_placeholder_image(os.path.join(media_root, 'events', 'gen_ai.png'), "Generative AI Workshop", (32, 201, 151))
    generate_placeholder_image(os.path.join(media_root, 'events', 'hackathon.png'), "Sunderland AI Hackathon", (253, 126, 20))
    generate_placeholder_image(os.path.join(media_root, 'events', 'retail_ai.png'), "AI in Retail Webinar", (111, 66, 193))
    
    generate_placeholder_image(os.path.join(media_root, 'blogs', 'modern_office.png'), "Modern Office AI", (13, 110, 253))
    generate_placeholder_image(os.path.join(media_root, 'blogs', 'prototyping.png'), "AI Prototyping Guide", (0, 210, 255))
    generate_placeholder_image(os.path.join(media_root, 'blogs', 'big_data.png'), "Big Data Analytics", (253, 126, 20))
    
    generate_placeholder_image(os.path.join(media_root, 'gallery', 'launch.png'), "Sunderland AI Launch", (13, 110, 253))
    generate_placeholder_image(os.path.join(media_root, 'gallery', 'workshop.png'), "Developer Workshop", (32, 201, 151))
    generate_placeholder_image(os.path.join(media_root, 'gallery', 'hack_team.png'), "Hackathon Team", (253, 126, 20))
    generate_placeholder_image(os.path.join(media_root, 'gallery', 'panel.png'), "Q&A Panel Discussion", (111, 66, 193))
    
    # 1. Create Case Studies
    print("Creating Case Studies...")
    CaseStudy.objects.create(
        title="AI-Powered Predictive Maintenance for Sunderland Manufacturing",
        objective="Reduce downtime in heavy machinery operation by implementing a real-time IoT and anomaly detection solution.",
        technologies_used="Python, TensorFlow, Django REST Framework, PostgreSQL",
        outcomes="Achieved a 25% reduction in unplanned equipment downtime and saved over £50k in maintenance costs in the first six months.",
        image="case_studies/mfg_ai.png"
    )
    CaseStudy.objects.create(
        title="Automated Virtual Assistant for E-Commerce Scaleup",
        objective="Provide 24/7 customer service support, handle order queries, and capture warm leads autonomously.",
        technologies_used="Django, NLP, JavaScript, Bootstrap 5",
        outcomes="Handled 78% of incoming queries without human intervention, boosting customer satisfaction scores by 15%.",
        image="case_studies/ecom_ai.png"
    )
    CaseStudy.objects.create(
        title="Intelligent Supply Chain Forecasting Platform",
        objective="Predict material demand spikes and optimize warehousing storage for a regional logistics provider.",
        technologies_used="Python, Scikit-learn, Pandas, PostgreSQL",
        outcomes="Improved stock levels accuracy by 18%, resulting in lower storage overhead and faster delivery turnaround.",
        image="case_studies/supply_ai.png"
    )
    
    # 2. Create Events
    print("Creating Events...")
    today = datetime.date.today()
    Event.objects.create(
        title="Introduction to Generative AI for Small Businesses Workshop",
        description="A hands-on workshop designed to help local startups understand and implement generative AI tools in their daily workflows.",
        date=today + datetime.timedelta(days=14),
        time=datetime.time(14, 0),
        location="AI-Solutions Hub, Sunderland",
        max_attendees=50,
        is_active=True,
        image="events/gen_ai.png"
    )
    Event.objects.create(
        title="Sunderland AI Hackathon 2026",
        description="Join developers, designers, and innovators to build cutting-edge AI prototyping solutions that solve digital employee experience problems.",
        date=today + datetime.timedelta(days=19),
        time=datetime.time(9, 30),
        location="Sunderland Software Centre, Sunderland",
        max_attendees=100,
        is_active=True,
        image="events/hackathon.png"
    )
    Event.objects.create(
        title="AI in Retail: Enhancing Customer Experience Seminar",
        description="A virtual panel discussion featuring industry leaders sharing insights on chatbots, predictive shopping, and automated inventories.",
        date=today - datetime.timedelta(days=22),
        time=datetime.time(16, 0),
        location="Online Webinar",
        max_attendees=250,
        is_active=True,
        image="events/retail_ai.png"
    )
    
    # 3. Create Feedback
    print("Creating Customer Feedback...")
    Feedback.objects.create(
        customer_name="Sarah Jenkins, Ops Director",
        rating=5,
        comment="AI-Solutions delivered an outstanding AI prototype for our factory line. Their rapid execution and professionalism exceeded our expectations!"
    )
    Feedback.objects.create(
        customer_name="David Cole, Tech Startup Founder",
        rating=4,
        comment="The Virtual Assistant integration has completely transformed our customer service flow. Clean, fast, and very easy to manage."
    )
    Feedback.objects.create(
        customer_name="Emma Watson, Operations Manager",
        rating=5,
        comment="Highly recommend their data management and predictive analytics solutions. The dashboard makes report analysis extremely straightforward."
    )
    Feedback.objects.create(
        customer_name="Marcus Aurelius, CEO of Nova Logistics",
        rating=5,
        comment="Their supply chain forecasting tool has saved us thousands in storage costs. Exceptional support throughout the project."
    )
    
    # 4. Create Blog Posts
    print("Creating Blog Posts...")
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        # Create a default admin user if it doesn't exist
        admin_user = User.objects.create_superuser('admin', 'admin@ai-solutions.tech', 'admin123')
        print("Created superuser: admin / admin123")
        
    BlogPost.objects.create(
        title="How AI is Reshaping the Modern Office Environment",
        slug="how-ai-reshaping-modern-office",
        excerpt="Understand how artificial intelligence is improving standard internal procedures and reducing administrative friction.",
        content="Artificial Intelligence is no longer a concept for the distant future. From automated virtual assistants that schedule meetings to predictive data analytics that support business planning, AI tools are actively improving employee experiences. In this article, we outline key ways technology start-ups can leverage conversational agents to streamline standard internal procedures and reduce administrative friction.",
        author=admin_user,
        author_name="Sarah Mitchell",
        author_role="AI Solutions Writer",
        published_date=timezone.now() - datetime.timedelta(days=10),
        is_published=True,
        featured_image="blogs/modern_office_team.png"
    )
    BlogPost.objects.create(
        title="Rapid Prototyping: The Secret to Successful AI Ventures",
        slug="rapid-prototyping-secret-ai-ventures",
        excerpt="Building functional, small-scale models allows you to validate theories and gather user feedback cost-effectively.",
        content="Many companies spend months and thousands of pounds building complex AI models only to find they don't align with actual business needs. Rapid prototyping offers a cost-effective alternative: building functional, small-scale models to validate theories, gather user feedback, and refine specifications before scaling up. This methodology is central to our work at AI-Solutions.",
        author=admin_user,
        author_name="Elena Rodriguez",
        author_role="Chief AI Scientist",
        published_date=timezone.now() - datetime.timedelta(days=5),
        is_published=True,
        featured_image="blogs/ai_prototyping.png"
    )
    BlogPost.objects.create(
        title="Unlocking Value in Big Data with Django and PostgreSQL",
        slug="unlocking-value-big-data-django-postgresql",
        excerpt="Analyze gigabytes of inquiry and customer data in real time, turning raw info into helpful business dashboard insights.",
        content="Handling structured database tables efficiently is a cornerstone of modern software systems. By using Django's ORM and PostgreSQL's robust querying engine, developers can analyze gigabytes of inquiry and customer data in real time, turning raw info into helpful business dashboard insights. Here is how we build security-conscious, performant databases for our clients.",
        author=admin_user,
        author_name="John Smith",
        author_role="Lead Data Engineer",
        published_date=timezone.now(),
        is_published=True,
        featured_image="blogs/big_data_analytics.png"
    )
    
    # 5. Create Gallery Images
    print("Creating Gallery Images...")
    GalleryImage.objects.create(
        title="Sunderland AI Launch Event",
        image="gallery/launch.png"
    )
    GalleryImage.objects.create(
        title="Interactive Developer Workshop",
        image="gallery/workshop.png"
    )
    GalleryImage.objects.create(
        title="Active Hackathon Team Collaboration",
        image="gallery/hack_team.png"
    )
    GalleryImage.objects.create(
        title="Q&A Panel Discussion with Experts",
        image="gallery/panel.png"
    )
    
    # 6. Create Customer Inquiries
    print("Creating Customer Inquiries...")
    # Seed inquiries spread across the last 6 months to populate the charts
    inquiries_data = [
        ("John Doe", "john@microsoft.com", "+1 555-019-2834", "AI Consulting", "Interested in AI prototyping solutions.", "New", today - datetime.timedelta(days=120)),
        ("Aiko Tanaka", "aiko@toyota.jp", "+81 90-1234-5678", "Automation", "Looking for virtual assistant setups.", "In Progress", today - datetime.timedelta(days=90)),
        ("Pierre Dubois", "pierre@carrefour.fr", "+33 1 42 27 78 90", "Analytics", "Need data analytics tools for retail.", "Resolved", today - datetime.timedelta(days=60)),
        ("Sarah Jenkins", "sarah@nissan.co.uk", "+44 7911 123456", "Other", "Nissan inquiry about customized models.", "New", today - datetime.timedelta(days=30)),
        ("Liam O'Connor", "liam@sunderlandcity.gov.uk", "+44 191 555 7788", "AI Consulting", "Council needs chatbot prototype.", "New", today - datetime.timedelta(days=10)),
        ("Emma Smith", "emma@sunderlandtech.com", "+44 7722 987654", "Automation", "Automate invoice scanning pipeline.", "In Progress", today - datetime.timedelta(days=5)),
        ("Robert Vance", "bob@vance refrigeration.com", "+1 555-901-2234", "Analytics", "Refrigeration analytics optimization.", "New", today)
    ]
    
    for name, email, phone, service, msg, status, created_date in inquiries_data:
        inq = CustomerInquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            service_interest=service,
            message=msg,
            status=status,
            notes="Seeded automatically."
        )
        # Bypassing auto_now_add to backdate created_at
        CustomerInquiry.objects.filter(pk=inq.pk).update(created_at=timezone.make_aware(datetime.datetime.combine(created_date, datetime.time.min)))

    # 7. Create Contact Messages
    print("Creating Contact Messages...")
    # Seed contact messages spread across the last 4 weeks
    messages_data = [
        ("Alice Cooper", "alice@music.com", "General Question", "How can I partner with you?", True, today - datetime.timedelta(days=25)),
        ("Bob Marley", "bob@reggae.com", "Service Pricing", "What are the rates for virtual assistants?", False, today - datetime.timedelta(days=18)),
        ("Charlie Chaplin", "charlie@silent.com", "Consulting Inquiry", "Are your consultants available next month?", True, today - datetime.timedelta(days=11)),
        ("Diana Prince", "diana@justice.org", "Security Inquiry", "What data compliance standards do you follow?", False, today - datetime.timedelta(days=4)),
        ("Ethan Hunt", "ethan@imf.gov", "Mission critical inquiry", "Need immediate AI prototyping session.", False, today)
    ]
    
    for name, email, subject, msg, is_read, submitted_date in messages_data:
        cmsg = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=msg,
            is_read=is_read
        )
        # Bypassing auto_now_add to backdate submitted_at
        ContactMessage.objects.filter(pk=cmsg.pk).update(submitted_at=timezone.make_aware(datetime.datetime.combine(submitted_date, datetime.time.min)))
    
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
