from django.shortcuts import render

def company_registration(request):
    return render(request, 'company/company_registration.html', {'title': 'Company registration'})
