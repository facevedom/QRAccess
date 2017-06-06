from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.core.mail import send_mail

from django.contrib.auth.models import User
from app.models import Company

from app.forms import CompanyForm


def company_registration(request):

    if request.method == 'GET':
        form = CompanyForm()
        return render(request, 'company/company_registration.html', {'title': 'Company registration', 'form': form})



    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Company.objects.create(
                email = data['email'], 
                telephone = data['telephone'],
                name = data['name'],
                address = data['address']
            )
            User.objects.create_user(
                username=data['name'], 
                password= data['password'], 
                email=data['email']
            )
            send_validation_email(data['email'])
            return success_happened(request, 'Company {company} successfuly created'.format(company=data['name']))
        return render(request, 'company/company_registration.html', {'title': 'Company registration', 'form': form})

    return Http404()



def send_validation_email(email):
    subject = 'QRAccess - Please confirm your email address'
    message = '''Thanks for signing up for QRAccess! Please click the link below 
              to confirm your mail address.
              \nhttp://127.0.0.1/account_verification/ 
              \n
              \nTeam QRAccess'''
    html_message = '''Thanks for signing up for QRAccess! Please click this 
                   <a http://127.0.0.1/account_verification/>link</a> to confirm your mail address.
                   \n
                   \nTeam QRAccess'''
    _from = 'noreply.qraccess@gmail.com'
    to = [email]

    send_mail(subject, message, _from, to, fail_silently=False, html_message=html_message)