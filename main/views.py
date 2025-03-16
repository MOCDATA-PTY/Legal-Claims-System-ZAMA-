from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ShipmentForm, LoginForm, RegisterForm
from .models import Shipment
import openpyxl
import datetime
from django.db import IntegrityError

# Redirect root URL to login page
def index(request):
    return redirect('login')

# Home page view - requires login
@login_required(login_url='login')
def home(request):
    return render(request, 'main/home.html')

# View for handling the creation of new shipments with duplicate `Claim_No` prevention
@login_required(login_url='login')
def add_shipment(request):
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        claim_no = request.POST.get('Claim_No')

        # Check if a shipment with the same Claim_No already exists
        existing_shipment = Shipment.objects.filter(Claim_No=claim_no).first()

        if existing_shipment:
            # Return the edit page link if a duplicate exists
            return render(request, 'main/add_shipment.html', {
                'form': form,
                'duplicate_claim_no': claim_no,
                'edit_shipment_id': existing_shipment.id,  # Pass the shipment ID to the template
                'show_popup': True  # Flag to show the popup
            })

        if form.is_valid():
            form.save()
            messages.success(request, "Shipment added successfully!")
            return redirect('shipment_list')

    else:
        form = ShipmentForm()

    return render(request, 'main/add_shipment.html', {'form': form})

# View for listing all shipments


# View for listing all shipments with filtering
@login_required(login_url='login')
def shipment_list(request):
    # Start with all shipments
    shipments = Shipment.objects.all()
    
    # Get unique branches for dropdown
    branches = Shipment.objects.values_list('Branch', flat=True).distinct().order_by('Branch')
    
    # Apply filters if provided
    if request.GET:
        # Filter by claim number
        if claim_no := request.GET.get('claim_no'):
            shipments = shipments.filter(Claim_No__icontains=claim_no)
        
        # Filter by claiming client
        if client := request.GET.get('client'):
            shipments = shipments.filter(Claiming_Client__icontains=client)
        
        # Filter by branch
        if branch := request.GET.get('branch'):
            shipments = shipments.filter(Branch=branch)
        
        # Filter by formal claim status
        if formal_claim := request.GET.get('formal_claim'):
            formal_claim_bool = formal_claim == 'True'
            shipments = shipments.filter(Formal_Claim_Received=formal_claim_bool)
        
        # Filter by date range for Intend Date
        if intend_date_from := request.GET.get('intend_date_from'):
            try:
                intend_date_from = datetime.datetime.strptime(intend_date_from, '%Y-%m-%d').date()
                shipments = shipments.filter(Intend_Claim_Date__gte=intend_date_from)
            except ValueError:
                pass  # Invalid date format, ignore filter
        
        if intend_date_to := request.GET.get('intend_date_to'):
            try:
                intend_date_to = datetime.datetime.strptime(intend_date_to, '%Y-%m-%d').date()
                shipments = shipments.filter(Intend_Claim_Date__lte=intend_date_to)
            except ValueError:
                pass  # Invalid date format, ignore filter
        
        # Filter by date range for Formal Date
        if formal_date_from := request.GET.get('formal_date_from'):
            try:
                formal_date_from = datetime.datetime.strptime(formal_date_from, '%Y-%m-%d').date()
                shipments = shipments.filter(Formal_Claim_Date_Received__gte=formal_date_from)
            except ValueError:
                pass  # Invalid date format, ignore filter
        
        if formal_date_to := request.GET.get('formal_date_to'):
            try:
                formal_date_to = datetime.datetime.strptime(formal_date_to, '%Y-%m-%d').date()
                shipments = shipments.filter(Formal_Claim_Date_Received__lte=formal_date_to)
            except ValueError:
                pass  # Invalid date format, ignore filter
        
        # Filter by date range for Closed Date
        if closed_date_from := request.GET.get('closed_date_from'):
            try:
                closed_date_from = datetime.datetime.strptime(closed_date_from, '%Y-%m-%d').date()
                shipments = shipments.filter(Closed_Date__gte=closed_date_from)
            except ValueError:
                pass  # Invalid date format, ignore filter
        
        if closed_date_to := request.GET.get('closed_date_to'):
            try:
                closed_date_to = datetime.datetime.strptime(closed_date_to, '%Y-%m-%d').date()
                shipments = shipments.filter(Closed_Date__lte=closed_date_to)
            except ValueError:
                pass  # Invalid date format, ignore filter
        
        # Filter by amount ranges
        if claimed_amount_min := request.GET.get('claimed_amount_min'):
            try:
                claimed_amount_min = float(claimed_amount_min)
                shipments = shipments.filter(Claimed_Amount__gte=claimed_amount_min)
            except ValueError:
                pass  # Invalid number format, ignore filter
        
        if claimed_amount_max := request.GET.get('claimed_amount_max'):
            try:
                claimed_amount_max = float(claimed_amount_max)
                shipments = shipments.filter(Claimed_Amount__lte=claimed_amount_max)
            except ValueError:
                pass  # Invalid number format, ignore filter
        
        # Filter by amount paid by carrier
        if carrier_amount_min := request.GET.get('carrier_amount_min'):
            try:
                carrier_amount_min = float(carrier_amount_min)
                shipments = shipments.filter(Amount_Paid_By_Carrier__gte=carrier_amount_min)
            except ValueError:
                pass
        
        if carrier_amount_max := request.GET.get('carrier_amount_max'):
            try:
                carrier_amount_max = float(carrier_amount_max)
                shipments = shipments.filter(Amount_Paid_By_Carrier__lte=carrier_amount_max)
            except ValueError:
                pass
        
        # Filter by amount paid by AWA
        if awa_amount_min := request.GET.get('awa_amount_min'):
            try:
                awa_amount_min = float(awa_amount_min)
                shipments = shipments.filter(Amount_Paid_By_Awa__gte=awa_amount_min)
            except ValueError:
                pass
        
        if awa_amount_max := request.GET.get('awa_amount_max'):
            try:
                awa_amount_max = float(awa_amount_max)
                shipments = shipments.filter(Amount_Paid_By_Awa__lte=awa_amount_max)
            except ValueError:
                pass
        
        # Filter by amount paid by insurance
        if insurance_amount_min := request.GET.get('insurance_amount_min'):
            try:
                insurance_amount_min = float(insurance_amount_min)
                shipments = shipments.filter(Amount_Paid_By_Insurance__gte=insurance_amount_min)
            except ValueError:
                pass
        
        if insurance_amount_max := request.GET.get('insurance_amount_max'):
            try:
                insurance_amount_max = float(insurance_amount_max)
                shipments = shipments.filter(Amount_Paid_By_Insurance__lte=insurance_amount_max)
            except ValueError:
                pass
    
    context = {
        'shipments': shipments,
        'branches': branches,
    }
    return render(request, 'main/shipment_list.html', context)




# View for editing an existing shipment
@login_required(login_url='login')
def edit_shipment(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)  # Make sure the instance is passed to the form
        if form.is_valid():
            form.save()
            messages.success(request, "Shipment updated successfully!")
            return redirect('shipment_list')  # Redirect back to the shipment list after saving
        else:
            # If form is not valid, we want to re-render the form with error messages
            messages.error(request, "There were errors in the form. Please fix them and try again.")
    else:
        form = ShipmentForm(instance=shipment)  # On GET request, load the existing shipment data in the form

    return render(request, 'main/edit_shipment.html', {'form': form, 'shipment': shipment})

# View to export shipments data to Excel
@login_required(login_url='login')
def export_shipments_excel(request):
    shipments = Shipment.objects.all()
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Shipments'
    headers = ['Claim No', 'Claiming Client', 'Branch', 'Formal Claim', 'Intend Date', 
               'Formal Date', 'Claimed Amount', 'Amount Paid by Carrier', 
               'Amount Paid by AWA', 'Amount Paid by Insurance', 'Closed Date']
    worksheet.append(headers)
    
    for shipment in shipments:
        worksheet.append([ 
            shipment.Claim_No,
            shipment.Claiming_Client,
            shipment.Branch,
            shipment.Formal_Claim_Received,
            shipment.Intend_Claim_Date.strftime("%Y-%m-%d") if shipment.Intend_Claim_Date else '',
            shipment.Formal_Claim_Date_Received.strftime("%Y-%m-%d") if shipment.Formal_Claim_Date_Received else '',
            float(shipment.Claimed_Amount),
            float(shipment.Amount_Paid_By_Carrier),
            float(shipment.Amount_Paid_By_Awa),
            float(shipment.Amount_Paid_By_Insurance),
            shipment.Closed_Date.strftime("%Y-%m-%d") if shipment.Closed_Date else ''
        ])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=shipments.xlsx'
    workbook.save(response)
    
    return response

# View to import shipments data from Excel with duplicate prevention
@login_required(login_url='login')
def import_shipments(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        try:
            excel_file = request.FILES['excel_file']
            
            # Check if the file is an Excel file
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                messages.error(request, "File must be an Excel file (.xlsx or .xls)")
                return render(request, 'main/import_shipments.html')
                
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb.active

            skipped_entries = []
            created_entries = 0
            error_entries = []

            # Extract headers to make sure they match expected format
            headers = [cell.value for cell in worksheet[1]]
            expected_headers = ['Claim', 'Claiming Client', 'Branch', 'Formal Claim', 'Intend Date', 
                               'Formal Date', 'Claimed Amount', 'Amount Paid by Carrier', 
                               'Amount Paid by AWA', 'Amount Paid by Insurance', 'Closed Date']
            
            # Check if headers match expected format
            if not all(header in headers for header in expected_headers):
                messages.error(request, "Excel file headers do not match the expected format")
                return render(request, 'main/import_shipments.html')

            for row in worksheet.iter_rows(min_row=2, values_only=True):
                if not row[0]:  # Skip empty rows
                    continue
                    
                claim_no = str(row[0])  # Convert to string in case it's a number in Excel
                
                # Check if Claim_No already exists
                if Shipment.objects.filter(Claim_No=claim_no).exists():
                    skipped_entries.append(claim_no)
                    continue
                
                try:
                    # Map Excel columns to model fields
                    Shipment.objects.create(
                        Claim_No=claim_no,
                        Claiming_Client=row[1] if row[1] else "",
                        Branch=row[2] if row[2] else "",
                        Formal_Claim_Received=row[3] if row[3] else False,
                        Intend_Claim_Date=row[4] if isinstance(row[4], datetime.date) else None,
                        Formal_Claim_Date_Received=row[5] if isinstance(row[5], datetime.date) else None,
                        Claimed_Amount=float(row[6]) if row[6] else 0.0,
                        Amount_Paid_By_Carrier=float(row[7]) if row[7] else 0.0,
                        Amount_Paid_By_Awa=float(row[8]) if row[8] else 0.0,
                        Amount_Paid_By_Insurance=float(row[9]) if row[9] else 0.0,
                        Closed_Date=row[10] if isinstance(row[10], datetime.date) else None
                    )
                    created_entries += 1
                except (ValueError, IntegrityError, TypeError) as e:
                    error_entries.append(f"{claim_no}: {str(e)}")

            if created_entries:
                messages.success(request, f"{created_entries} shipments imported successfully!")

            if skipped_entries:
                messages.warning(request, f"{len(skipped_entries)} duplicate shipments were skipped.")
            
            if error_entries:
                messages.error(request, f"{len(error_entries)} entries had errors and could not be imported.")

            context = {
                'skipped_entries': skipped_entries,
                'error_entries': error_entries,
                'success_count': created_entries
            }
            return render(request, 'main/import_shipments.html', context)
            
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'main/import_shipments.html')
    
    return render(request, 'main/import_shipments.html')

# View to fetch client names dynamically based on the user's query
@login_required(login_url='login')
def get_client_names(request):
    query = request.GET.get('q', '')
    clients = Shipment.objects.filter(
        Claiming_Client__icontains=query
    ).order_by('Claiming_Client').values_list('Claiming_Client', flat=True).distinct()
    return JsonResponse(list(clients), safe=False)

# User authentication views
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session.set_expiry(0)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session.set_expiry(0)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


    