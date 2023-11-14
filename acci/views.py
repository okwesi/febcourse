from django.shortcuts import render, redirect
from .models import Attendee
from django.http import HttpResponse
import pandas as pd
from django import forms



class AttendeeForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    tag_number = forms.CharField(label='Tag Number', max_length=20)
    telephone = forms.CharField(label='Telephone Number', max_length=15)
    area = forms.CharField(label='Area', max_length=100)
    district = forms.CharField(label='District', max_length=100)
    local_assembly = forms.CharField(label='Local Assembly', max_length=100)
    position = forms.CharField(label='Position', max_length=100)
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)



def create_person(request):
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            # Save the data to the database
            data = form.cleaned_data
            
            attendee = Attendee.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                tag_number=data['tag_number'],
                telephone=data['telephone'],
                area=data['area'],
                district=data['district'],
                local_assembly=data['local_assembly'],
                position=data['position'],
                amount=data['amount']
            )
            return redirect('/success')

    else:
        form = AttendeeForm()

    return render(request, 'create_person.html', {'form': form})

def success_page(request):
    return render(request, 'success.html')


def all_attendees(request):
    attendees = Attendee.objects.all()
    return render(request, 'person_list.html', {'attendees': attendees})


def clear_database(request):
    if request.method == 'POST':
        Attendee.objects.all().delete()
        return redirect('/list')

    return render(request, 'person_list.html')



def download_excel(request):
    # Get all attendees from the database
    attendees = Attendee.objects.all()

    # Convert attendees data to a DataFrame
    data = {
        'First Name': [attendee.first_name for attendee in attendees],
        'Last Name': [attendee.last_name for attendee in attendees],
        'Tag Number': [attendee.tag_number for attendee in attendees],
        'Telephone': [attendee.telephone for attendee in attendees],
        'Area': [attendee.area for attendee in attendees],
        'District': [attendee.district for attendee in attendees],
        'Local Assembly': [attendee.local_assembly for attendee in attendees],
        'Position': [attendee.position for attendee in attendees],
        'Amount': [attendee.amount for attendee in attendees],
    }
    df = pd.DataFrame(data)

    # Create a BytesIO object to store Excel file
    excel_file = pd.ExcelWriter('attendees_data.xlsx', engine='openpyxl')
    df.to_excel(excel_file, index=False)
    excel_file.save()

    # Create a response with the Excel file
    with open('attendees_data.xlsx', 'rb') as excel_data:
        response = HttpResponse(excel_data.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=attendees_data.xlsx'
        return response