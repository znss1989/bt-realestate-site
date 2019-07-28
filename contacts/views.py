from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact


# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check if user make same inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'Have inquired this already')
                return redirect('/listings/' + listing_id)
        # record the contact/inquiry
        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
        contact.save()
        # # send email
        # send_mail(
        #     'Property Listing Inquiry',
        #     'There has been an inquiry for ' + listing + '. Sign into the admin panel, for more info.',
        #     'test@gmail.com',
        #     [realtor_email],
        #     fail_silently=True
        # )

        messages.success(request, 'Request sent, a realtor will get to you soon.')
        return redirect('/listings/' + listing_id)
