from django.urls import path
from . import views

urlpatterns = [
    # Public Client-Facing Routes
    path('wireframe/home/', views.WireframeHomeView.as_view(), name='wireframe_home'),
    path('wireframe/chatbot/', views.WireframeChatbotView.as_view(), name='wireframe_chatbot'),
    path('', views.home, name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('past-solutions/', views.PastSolutionsView.as_view(), name='past_solutions'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms_of_service'),
    path('case-studies/', views.CaseStudyListView.as_view(), name='case_studies'),
    path('events/', views.events_view, name='events'),
    path('feedback/', views.FeedbackListView.as_view(), name='feedback'),
    path('gallery/', views.GalleryListView.as_view(), name='gallery'),
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('chatbot/query/', views.chatbot_query, name='chatbot_query'),
    
    # Custom Staff Authentication
    path('dashboard/login/', views.DashboardLoginView.as_view(), name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    
    # Main Dashboard Landing
    path('dashboard/', views.DashboardHomeView.as_view(), name='dashboard'),
    
    # Customer Inquiry CRUD
    path('dashboard/inquiries/', views.InquiryListView.as_view(), name='inquiry_list'),
    path('dashboard/inquiries/add/', views.InquiryCreateView.as_view(), name='inquiry_add'),
    path('dashboard/inquiries/<int:pk>/', views.InquiryDetailView.as_view(), name='inquiry_detail'),
    path('dashboard/inquiries/<int:pk>/edit/', views.InquiryUpdateView.as_view(), name='inquiry_edit'),
    path('dashboard/inquiries/<int:pk>/delete/', views.InquiryDeleteView.as_view(), name='inquiry_delete'),
    
    # Contact Message CRUD
    path('dashboard/contacts/', views.ContactListView.as_view(), name='contact_list'),
    path('dashboard/contacts/mark-all-read/', views.mark_all_contacts_read, name='contact_mark_all_read'),
    path('dashboard/contacts/<int:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('dashboard/contacts/<int:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
    
    # BlogPost CRUD
    path('dashboard/blog/', views.BlogPostListView.as_view(), name='blog_list'),
    path('dashboard/blog/add/', views.BlogPostCreateView.as_view(), name='blog_add'),
    path('dashboard/blog/<int:pk>/edit/', views.BlogPostUpdateView.as_view(), name='blog_edit'),
    path('dashboard/blog/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='blog_delete'),
    
    # Event CRUD
    path('dashboard/events/', views.EventDashboardListView.as_view(), name='event_list'),
    path('dashboard/events/add/', views.EventCreateView.as_view(), name='event_add'),
    path('dashboard/events/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('dashboard/events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('dashboard/events/<int:event_id>/registrations/', views.event_registrations, name='event_registrations'),
    path('register-event/', views.register_event, name='register_event'),
    
    # Feedback CRUD
    path('dashboard/feedback/', views.feedback_list, name='feedback_list'),
    path('dashboard/feedback/add/', views.FeedbackCreateView.as_view(), name='feedback_add'),
    
    # Gallery CRUD
    path('dashboard/gallery/', views.gallery_list, name='gallery_list'),
    path('dashboard/gallery/upload/', views.GalleryImageCreateView.as_view(), name='gallery_upload'),
    path('dashboard/gallery/<int:pk>/edit/', views.GalleryImageUpdateView.as_view(), name='gallery_edit'),

    # Change Password
    path('dashboard/change-password/', views.change_password, name='change_password'),
]
