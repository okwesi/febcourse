from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendee
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
from django import forms
from django.urls import reverse
from django.http import JsonResponse



class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = '__all__'


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
    total_attendees = attendees.count()  
    return render(request, 'person_list.html', {'attendees': attendees, 'total_attendees': total_attendees})

def clear_database(request):
    if request.method == 'POST':
        Attendee.objects.all().delete()
        return redirect('/list')

    return render(request, 'person_list.html')


def edit_attendee(request, attendee_id):
    attendee = get_object_or_404(Attendee, pk=attendee_id)

    if request.method == 'POST':
        form = AttendeeForm(request.POST, instance=attendee)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('all_attendees'))
    else:
        form = AttendeeForm(instance=attendee)

    return render(request, 'edit_attendee.html', {'form': form, 'attendee': attendee})


@csrf_exempt
def delete_attendee(request, attendee_id):
    if request.method == 'POST':
        attendee = get_object_or_404(Attendee, pk=attendee_id)
        attendee.delete()
        return JsonResponse({'success': True})
    
    

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