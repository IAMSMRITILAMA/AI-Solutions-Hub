from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Q, Count
from django.urls import reverse_lazy, reverse
from .models import CaseStudy, Event, Feedback, BlogPost, GalleryImage, CustomerInquiry, ContactMessage, EventRegistration
from .forms import PublicContactForm, CustomerInquiryForm, BlogPostForm, EventForm, FeedbackForm, GalleryImageForm
import json
import csv
import datetime

# --- Public Views ---

class WireframeHomeView(TemplateView):
    template_name = 'core/wireframe_home.html'

class WireframeChatbotView(TemplateView):
    template_name = 'core/wireframe_chatbot.html'

def home(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(
        is_active=True,
        date__gte=today
    ).order_by('date')[:2]
    latest_blogs = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3]
    gallery_photos = GalleryImage.objects.all()[:5]
    gallery_count = GalleryImage.objects.count()
    return render(request, 'core/home.html', {
        'upcoming_events': upcoming_events,
        'latest_blogs': latest_blogs,
        'gallery_photos': gallery_photos,
        'gallery_count': gallery_count,
    })


class AboutView(TemplateView):
    template_name = 'core/about.html'

class ServicesView(TemplateView):
    template_name = 'core/services.html'

class PastSolutionsView(TemplateView):
    template_name = 'core/past_solutions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['case_studies'] = CaseStudy.objects.all().order_by('-created_at')
        return context

class PrivacyPolicyView(TemplateView):
    template_name = 'core/privacy_policy.html'

class TermsOfServiceView(TemplateView):
    template_name = 'core/terms_of_service.html'

class CaseStudyListView(ListView):
    model = CaseStudy
    template_name = 'core/case_studies.html'
    context_object_name = 'case_studies'

def events_view(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(
        is_active=True,
        date__gte=today
    ).order_by('date')
    
    past_events = Event.objects.filter(
        is_active=True,
        date__lt=today
    ).order_by('-date')
    
    events = list(upcoming_events) + list(past_events)
    
    return render(request, 'core/events.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'events': events,
    })

class FeedbackListView(CreateView):
    model = Feedback
    fields = ['customer_name', 'rating', 'comment']
    template_name = 'core/feedback.html'
    success_url = '/feedback/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedbacks'] = Feedback.objects.order_by('-date')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Thank you for your feedback!")
        return super().form_valid(form)

class GalleryListView(ListView):
    model = GalleryImage
    template_name = 'core/gallery.html'
    context_object_name = 'images'

class BlogListView(ListView):
    model = BlogPost
    template_name = 'core/blog.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-published_date')

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'core/blog_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

def contact_view(request):
    if request.method == 'POST':
        form = PublicContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            service_interest = form.cleaned_data['service_interest']
            message = form.cleaned_data['message']

            # Save to CustomerInquiry
            CustomerInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                service_interest=service_interest,
                message=message,
                status='New'
            )

            # Save to ContactMessage
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=f"Inquiry: {service_interest}",
                message=message
            )

            messages.success(request, "Your inquiry has been submitted successfully. We will get back to you soon!")
            return redirect('contact')
    else:
        form = PublicContactForm()
    return render(request, 'core/contact.html', {'form': form})

# --- Chatbot View ---

def chatbot_query(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '').strip()
            query_lower = query.lower()
            
            state = request.session.get('chat_state')
            
            if state == 'collect_name':
                request.session['chat_name'] = query
                request.session['chat_state'] = 'collect_email'
                return JsonResponse({'response': f"Thanks, {query}! What is your email address?"})
                
            elif state == 'collect_email':
                request.session['chat_email'] = query
                request.session['chat_state'] = 'collect_details'
                return JsonResponse({'response': "Got it. Please describe your project or what you would like to discuss with our human representative."})
                
            elif state == 'collect_details':
                # Save the inquiry to database
                CustomerInquiry.objects.create(
                    name=request.session.get('chat_name', 'Chatbot User'),
                    email=request.session.get('chat_email', 'chatbot@user.com'),
                    phone='Collected via Chatbot',
                    service_interest='Automation',
                    message=f"Inquiry collected via chatbot: {query}",
                    status='New'
                )
                
                # Clear session
                request.session['chat_state'] = None
                request.session['chat_name'] = None
                request.session['chat_email'] = None
                
                return JsonResponse({'response': "Thank you! I have recorded your details and transferred them to our support queue. A representative will contact you shortly."})
            
            if query_lower in ['hello', 'hi', 'hey']:
                return JsonResponse({'response': "Hello! I am the AI-Solutions Virtual Assistant. How can I help you today?"})
                
            elif 'service' in query_lower or 'product' in query_lower:
                return JsonResponse({'response': "We offer AI Prototyping, Virtual Assistants, and Data Analytics. You can check our Services page for more info!"})
                
            elif 'contact' in query_lower or 'phone' in query_lower or 'email' in query_lower:
                return JsonResponse({'response': "You can email us at hello@ai-solutions.tech, call +44 191 123 4567, or fill out the form on our Contact page."})
                
            elif query_lower in ['human', 'transfer', 'representative', 'support', 'talk to human', 'yes']:
                request.session['chat_state'] = 'collect_name'
                return JsonResponse({'response': "Certainly! I can transfer this conversation to a human representative. First, what is your full name?"})
                
            else:
                return JsonResponse({'response': "I am here to answer basic questions about our services or contact information. Would you like to be transferred to a human representative? (Type 'yes' or 'human' to proceed)"})
                
        except Exception as e:
            return JsonResponse({'error': f'Error processing query: {str(e)}'}, status=400)
            
    return JsonResponse({'error': 'Invalid request method'}, status=400)

# --- Admin Dashboard & Auth Views ---

class DashboardLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

@login_required
def dashboard_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

@method_decorator(login_required, name='dispatch')
class DashboardHomeView(TemplateView):
    template_name = 'core/dashboard_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Stats Cards
        context['total_inquiries'] = CustomerInquiry.objects.count()
        context['new_inquiries'] = CustomerInquiry.objects.filter(status='New').count()
        context['unread_contacts'] = ContactMessage.objects.filter(is_read=False).count()
        context['resolved_inquiries'] = CustomerInquiry.objects.filter(status='Resolved').count()
        
        # Recent activity (5 most recent)
        context['recent_inquiries'] = CustomerInquiry.objects.order_by('-created_at')[:5]
        context['recent_contacts'] = ContactMessage.objects.order_by('-submitted_at')[:5]
        
        # Charts Data Calculations
        today = datetime.date.today()
        
        # 1. Bar Chart: Inquiries per month (last 6 months)
        bar_labels = []
        bar_data = []
        for i in range(5, -1, -1):
            m = today.month - i
            y = today.year
            if m <= 0:
                m += 12
                y -= 1
            dt = datetime.date(y, m, 1)
            bar_labels.append(dt.strftime("%b %Y"))
            count = CustomerInquiry.objects.filter(created_at__year=y, created_at__month=m).count()
            bar_data.append(count)
            
        context['bar_labels_json'] = json.dumps(bar_labels)
        context['bar_data_json'] = json.dumps(bar_data)
        
        # 2. Pie Chart: Inquiries by service_interest
        service_counts = CustomerInquiry.objects.values('service_interest').annotate(count=Count('id'))
        pie_labels = []
        pie_data = []
        for item in service_counts:
            pie_labels.append(item['service_interest'])
            pie_data.append(item['count'])
            
        # Fallback if no data
        if not pie_labels:
            pie_labels = ['AI Consulting', 'Automation', 'Analytics', 'Other']
            pie_data = [0, 0, 0, 0]
            
        context['pie_labels_json'] = json.dumps(pie_labels)
        context['pie_data_json'] = json.dumps(pie_data)
        
        # 3. Line Chart: Contact messages received per week (last 4 weeks)
        line_labels = []
        line_data = []
        for i in range(3, -1, -1):
            start_date = today - datetime.timedelta(weeks=i+1)
            end_date = today - datetime.timedelta(weeks=i)
            line_labels.append(f"Week {4-i}")
            count = ContactMessage.objects.filter(
                submitted_at__date__gte=start_date,
                submitted_at__date__lt=end_date
            ).count()
            line_data.append(count)
            
        context['line_labels_json'] = json.dumps(line_labels)
        context['line_data_json'] = json.dumps(line_data)
        
        return context

# --- Customer Inquiry CRUD Views ---

@method_decorator(login_required, name='dispatch')
class InquiryListView(ListView):
    model = CustomerInquiry
    template_name = 'core/inquiry_list.html'
    context_object_name = 'inquiries'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = CustomerInquiry.objects.all()
        
        # Search
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(email__icontains=q))
            
        # Sorting
        sort_by = self.request.GET.get('sort_by', '-created_at')
        allowed_sorts = ['created_at', '-created_at', 'status', '-status', 'name', '-name']
        if sort_by in allowed_sorts:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-created_at')
            
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['sort_by'] = self.request.GET.get('sort_by', '-created_at')
        return context

@method_decorator(login_required, name='dispatch')
class InquiryCreateView(CreateView):
    model = CustomerInquiry
    form_class = CustomerInquiryForm
    template_name = 'core/inquiry_form.html'
    success_url = reverse_lazy('inquiry_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Customer inquiry added successfully!")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class InquiryDetailView(DetailView):
    model = CustomerInquiry
    template_name = 'core/inquiry_detail.html'
    context_object_name = 'inquiry'

@method_decorator(login_required, name='dispatch')
class InquiryUpdateView(UpdateView):
    model = CustomerInquiry
    form_class = CustomerInquiryForm
    template_name = 'core/inquiry_form.html'
    success_url = reverse_lazy('inquiry_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Customer inquiry updated successfully!")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class InquiryDeleteView(DeleteView):
    model = CustomerInquiry
    template_name = 'core/inquiry_confirm_delete.html'
    success_url = reverse_lazy('inquiry_list')
    
    def post(self, request, *args, **kwargs):
        messages.success(request, "Customer inquiry deleted successfully!")
        return super().post(request, *args, **kwargs)

# --- Contact Message CRUD Views ---

@method_decorator(login_required, name='dispatch')
class ContactListView(ListView):
    model = ContactMessage
    template_name = 'core/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = ContactMessage.objects.all()
        
        # Search
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(subject__icontains=q))
            
        # Sorting
        sort_by = self.request.GET.get('sort_by', '-submitted_at')
        allowed_sorts = ['submitted_at', '-submitted_at', 'is_read', '-is_read', 'name', '-name']
        if sort_by in allowed_sorts:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-submitted_at')
            
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['sort_by'] = self.request.GET.get('sort_by', '-submitted_at')
        context['unread_count'] = ContactMessage.objects.filter(is_read=False).count()
        return context

@method_decorator(login_required, name='dispatch')
class ContactDetailView(DetailView):
    model = ContactMessage
    template_name = 'core/contact_detail.html'
    context_object_name = 'contact'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj

@method_decorator(login_required, name='dispatch')
class ContactDeleteView(DeleteView):
    model = ContactMessage
    template_name = 'core/contact_confirm_delete.html'
    success_url = reverse_lazy('contact_list')
    
    def post(self, request, *args, **kwargs):
        messages.success(request, "Contact message deleted successfully!")
        return super().post(request, *args, **kwargs)

@login_required
def mark_all_contacts_read(request):
    unread_messages = ContactMessage.objects.filter(is_read=False)
    count = unread_messages.count()
    unread_messages.update(is_read=True)
    messages.success(request, f"Marked {count} contact messages as read.")
    return redirect('contact_list')

# --- BlogPost CRUD Views ---

@method_decorator(login_required, name='dispatch')
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'core/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return BlogPost.objects.all().order_by('-published_date')

@method_decorator(login_required, name='dispatch')
class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'core/blog_form.html'
    success_url = reverse_lazy('blog_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Blog post created successfully!")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'core/blog_form.html'
    success_url = reverse_lazy('blog_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Blog post updated successfully!")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'core/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')
    
    def post(self, request, *args, **kwargs):
        messages.success(request, "Blog post deleted successfully!")
        return super().post(request, *args, **kwargs)

# --- Event CRUD Views ---

@method_decorator(login_required, name='dispatch')
class EventDashboardListView(ListView):
    model = Event
    template_name = 'core/event_list.html'
    context_object_name = 'events'
    paginate_by = 10
    
    def get_queryset(self):
        return Event.objects.all().order_by('-date')

@method_decorator(login_required, name='dispatch')
class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'core/event_form.html'
    success_url = reverse_lazy('event_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Event created successfully!")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'core/event_form.html'
    success_url = reverse_lazy('event_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Event updated successfully!")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'core/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')
    
    def post(self, request, *args, **kwargs):
        messages.success(request, "Event deleted successfully!")
        return super().post(request, *args, **kwargs)

# --- Feedback CRUD Views ---

@login_required
def feedback_list(request):
    # Handle Delete action
    delete_id = request.GET.get('delete_id')
    if delete_id:
        Feedback.objects.filter(id=delete_id).delete()
        messages.success(request, "Feedback deleted successfully.")
        return redirect('feedback_list')

    # Handle Toggle Featured action
    toggle_id = request.GET.get('toggle_id')
    if toggle_id:
        feedback = Feedback.objects.filter(id=toggle_id).first()
        if feedback:
            feedback.is_featured = not feedback.is_featured
            feedback.save()
            status = "featured" if feedback.is_featured else "unfeatured"
            messages.success(request, f"Feedback marked as {status}.")
        return redirect('feedback_list')

    feedbacks = Feedback.objects.all().order_by('-date', '-id')

    # Search by name
    q = request.GET.get('q', '').strip()
    if q:
        feedbacks = feedbacks.filter(customer_name__icontains=q)
        
    # Filter by rating
    rating = request.GET.get('rating')
    if rating and rating.isdigit():
        feedbacks = feedbacks.filter(rating=int(rating))

    context = {
        'feedbacks': feedbacks,
        'q': q,
        'rating': rating,
    }
    return render(request, 'core/feedback_list.html', context)

@method_decorator(login_required, name='dispatch')
class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'core/feedback_form.html'
    success_url = reverse_lazy('feedback_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Feedback added successfully!")
        return super().form_valid(form)

# --- Gallery CRUD Views ---

@login_required
def gallery_list(request):
    # Handle Delete action
    delete_id = request.GET.get('delete_id')
    if delete_id:
        GalleryImage.objects.filter(id=delete_id).delete()
        messages.success(request, "Photo deleted successfully.")
        return redirect('gallery_list')

    photos = GalleryImage.objects.all().order_by('-uploaded_date')

    # Filter by category
    category = request.GET.get('category')
    if category and category != 'All':
        photos = photos.filter(category=category)

    context = {
        'photos': photos,
        'category': category or 'All',
    }
    return render(request, 'core/gallery_list.html', context)


@method_decorator(login_required, name='dispatch')
class GalleryImageCreateView(CreateView):
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'core/gallery_form.html'
    success_url = reverse_lazy('gallery_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Photo uploaded successfully!")
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class GalleryImageUpdateView(UpdateView):
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'core/gallery_form.html'
    success_url = reverse_lazy('gallery_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Photo updated successfully!")
        return super().form_valid(form)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '✅ Password changed successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'core/change_password.html', {'form': form})


from django.views.decorators.http import require_POST

def register_event(request):
  if request.method == 'POST':
    EventRegistration.objects.create(
      event_id=request.POST['event_id'],
      full_name=request.POST['full_name'],
      email=request.POST['email'],
      phone=request.POST.get('phone','')
    )
    messages.success(request,
      '🎉 You have successfully registered for this event! We will contact you soon.')
  return redirect('events')


@login_required
def event_registrations(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = event.registrations.all().order_by('-registered_at')
    
    q = request.GET.get('q', '').strip()
    if q:
        registrations = registrations.filter(Q(full_name__icontains=q) | Q(email__icontains=q))
        
    context = {
        'event': event,
        'registrations': registrations,
        'q': q,
    }
    return render(request, 'core/event_registrations.html', context)