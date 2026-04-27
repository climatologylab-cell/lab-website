from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.conf import settings
from .models import ContactSubmission
import threading

def send_contact_emails_in_background(name, email, phone, query, submission_id):
    """Sends admin notification and user auto-reply independently via AWS SES API."""

    # --- Step 1: Always send admin notification ---
    try:
        from django.core.mail import EmailMessage
        admin_msg = EmailMessage(
            subject=f'New Contact Form Submission from {name}',
            body=f"New contact form submission received:\n\nName: {name}\nEmail: {email}\nPhone: {phone if phone else 'Not provided'}\n\nMessage/Query:\n{query}\n\n---\nSubmission ID: {submission_id}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )
        admin_msg.send()
        print(f"Admin notification sent for submission {submission_id}")
    except Exception as e:
        print(f"ERROR sending admin notification: {e}")

    # --- Step 2: Send user auto-reply (may fail in SES Sandbox if user email is unverified) ---
    try:
        from django.core.mail import EmailMessage
        user_msg = EmailMessage(
            subject='Thank You for Contacting Climatology Lab',
            body=f"Dear {name},\n\nThank you for connecting with us. We have received your query and will get back to you soon.\n\nYour Query:\n{query}\n\nWe appreciate your interest in the Climatology Lab and will respond as quickly as possible.\n\nBest regards,\n\nClimatology Lab\nDepartment of Architecture and Planning,\nIIT Roorkee, Roorkee (247667), Uttarakhand, India\nPhone: +91 - 1332-286141\nEmail: climatologylab@ar.iitr.ac.in",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        user_msg.send()
        print(f"User auto-reply sent to {email}")
    except Exception as e:
        # In SES Sandbox mode, unverified recipient emails will fail here.
        # This will be resolved once AWS Production Access is granted.
        print(f"ERROR sending user auto-reply to {email}: {e}")

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
        
        # Trigger background email task
        threading.Thread(
            target=send_contact_emails_in_background,
            args=(name, email, phone, query, submission.id)
        ).start()
        
        messages.success(request, 'Thank you for contacting us! We have sent a confirmation email to your address.')
        return redirect('core:home')
    
    return redirect('core:home')
