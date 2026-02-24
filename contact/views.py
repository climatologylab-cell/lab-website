from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import ContactSubmission

def contact_submit(request):
    """Handle contact form submission with email notifications"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        query = request.POST.get('query')
        
        # Create contact submission
        submission = ContactSubmission.objects.create(
            name=name,
            email=email,
            phone=phone,
            query=query
        )
        
        # Send email to admin
        try:
            admin_subject = f'New Contact Form Submission from {name}'
            admin_message = f"""
New contact form submission received:

Name: {name}
Email: {email}
Phone: {phone if phone else 'Not provided'}

Message/Query:
{query}

---
This email was sent from the Climatology Lab website contact form.
Submission ID: {submission.id}
            """
            
            send_mail(
                subject=admin_subject,
                message=admin_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
        except Exception as e:
            print(f"Error sending admin email: {e}")
        
        # Send auto-reply email to user
        try:
            user_subject = 'Thank You for Contacting Climatology Lab'
            user_message = f"""
Dear {name},

Thank you for connecting with us. We have received your query and will get back to you soon.

Your Query:
{query}

We appreciate your interest in the Climatology Lab and will respond to your inquiry as quickly as possible.

Best regards,
Climatology Lab
IIT Roorkee

---
This is an automated acknowledgment email. Please do not reply to this email.
If you have additional questions, please submit a new query through our website.
            """
            
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
        except Exception as e:
            print(f"Error sending user acknowledgment email: {e}")
        
        messages.success(request, 'Thank you for contacting us! We have sent a confirmation email to your address.')
        return redirect('core:home')
    
    return redirect('core:home')
