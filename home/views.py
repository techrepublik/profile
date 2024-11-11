import json
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.db.models.functions import ExtractYear, ExtractMonth, TruncYear
from .models import Unit, Department, Position, Item, Faculty
from .forms import UnitForm, DepartmentForm, PositionForm, ItemForm, FacultyForm, CustomLoginForm


@login_required
def employee_alpha_list(request):
    query = request.GET.get('q', '')
    employees = Faculty.objects.all()

    if query:
        employees = employees.filter(
            Q(faculty_no__icontains=query) |
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(gender__icontains=query) |
            Q(date_hired__icontains=query) |
            Q(item_no__icontains=query) |
            Q(employment_type__icontains=query) |
            Q(item_status__icontains=query) |
            Q(education__icontains=query) |
            Q(position_id__position_name__icontains=query) |
            Q(department_id__department_name__icontains=query) |
            Q(department_id__unit_id__unit_name__icontains=query)
        )

    if request.htmx:
        return render(request, 'reports/partial_alpha_list.html', {'employees': employees})

    return render(request, 'reports/faculty_list_report.html', {'employees': employees, 'query': query})

# unit


@login_required
def unit_chart_html(request):
    years = Faculty.objects.annotate(year=ExtractYear(
        'date_hired')).values('year').distinct().order_by('year')
    units = Unit.objects.filter(unit_type='Academic').distinct()
    # units = Unit.objects.filter(
    #     unit_department__department_faculty__employment_type='Teaching').distinct()
    return render(request, 'reports/chart_unit_report.html', {'years': years, 'units': units})


@login_required
def unit_admin_chart_html(request):
    years = Faculty.objects.annotate(year=ExtractYear(
        'date_hired')).values('year').distinct().order_by('year')
    units = Unit.objects.filter(unit_type='Administrative').distinct()
    # units = Unit.objects.filter(
    #     unit_department__department_faculty__employment_type='Teaching').distinct()
    return render(request, 'reports/chart_unit_admin_report.html', {'years': years, 'units': units})


def unit_chart_data(request, flag):
    year = request.GET.get('year_position')
    unit_id = request.GET.get('unit_id')

    if flag == 1:
        query = Faculty.objects.filter(
            is_active=True, department_id__unit_id__unit_type='Academic')
    else:
        query = Faculty.objects.filter(
            is_active=True, department_id__unit_id__unit_type='Administrative')

    if year and unit_id:
        query = query.filter(Q(date_hired__year=year) &
                             Q(department_id__unit_id=unit_id))
    elif year:
        query = query.filter(date_hired__year=year)
    elif unit_id:
        query = query.filter(department_id__unit_id=unit_id)

    print(query)

    position_counts = query.values('position_id__position_name').annotate(
        count=Count('id')).order_by('position_id__position_name')

    data = {
        'positions': [],
        'counts': []
    }

    for entry in position_counts:
        data['positions'].append(entry['position_id__position_name'])
        data['counts'].append(entry['count'])

    return JsonResponse(data)


def get_faculty_list(request, flag):
    year = request.GET.get('year_position')
    unit_id = request.GET.get('unit_id')

    if flag == 1:
        query = Faculty.objects.select_related(
            'position_id', 'department_id').filter(is_active=True, department_id__unit_id__unit_type='Academic')
    else:
        query = Faculty.objects.select_related(
            'position_id', 'department_id').filter(is_active=True, department_id__unit_id__unit_type='Administrative')

    if year and unit_id:
        query = query.filter(date_hired__year=year,
                             department_id__unit_id=unit_id)
    elif year:
        query = query.filter(date_hired__year=year)
    elif unit_id:
        query = query.filter(department_id__unit_id=unit_id)

    faculty_list = query.values(
        'faculty_no', 'item_no', 'last_name', 'first_name', 'middle_name', 'ext_name',
        'position_id__position_name', 'gender', 'item_status', 'department_id__department_name'
    ).order_by('last_name', 'first_name')

    data = {
        'faculty': []
    }

    for entry in faculty_list:
        name = f"{entry['last_name']}, {entry['first_name']} {entry['middle_name'][0] if entry['middle_name'] else ''} {entry['ext_name'] if entry['ext_name'] else ''}".strip()
        data['faculty'].append({
            'faculty_no': entry['faculty_no'],
            'item_no': entry['item_no'],
            'name': name,
            'position': entry['position_id__position_name'],
            'gender': entry['gender'],
            'item_status': entry['item_status'],
            'department_name': entry['department_id__department_name']
        })

    return JsonResponse(data)


# graph reports


def generate_status_graph_pdf(request):
    statuses = Faculty.objects.values_list('item_status', flat=True)
    status_counts = {
        'COS': statuses.filter(item_status='COS').count(),
        'Permanent': statuses.filter(item_status='Permanent').count(),
        'Vacant': statuses.filter(item_status='Vacant').count(),
    }

    # Render the HTML template with context data
    html_string = render_to_string('reports/chart_status_report.html', {
        'status_counts': status_counts
    })

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="chart_status_report.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    return response
    # return render(request, "reports/chart_status_report.html", {"status_counts": status_counts})

# reports


def generate_faculty_pdf(request):
    # Get faculty data categorized by gender
    males = Faculty.objects.filter(gender='Male', is_active=True)
    females = Faculty.objects.filter(gender='Female', is_active=True)

    # Render the HTML template with context data
    html_string = render_to_string('reports/faculty_list.html', {
        'males': males,
        'females': females
    })

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="faculty_list.pdf"'
    pisa_status = pisa.CreatePDF(
        html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    return response


def generate_faculty_type_pdf(request):
    # Get faculty data categorized by gender
    teaching = Faculty.objects.filter(
        employment_type='Teaching', is_active=True)
    non_teaching = Faculty.objects.filter(
        employment_type='Non-Teaching', is_active=True)

    # Render the HTML template with context data
    html_string = render_to_string('reports/faculty_list_type.html', {
        'teaching': teaching,
        'non_teaching': non_teaching
    })

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="faculty_type_list.pdf"'
    pisa_status = pisa.CreatePDF(
        html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    return response


def generate_faculty_education_pdf(request):
    # Get faculty data categorized by education
    education_levels = Faculty.EDUCATION
    faculty_by_education = {level[0]: Faculty.objects.filter(
        education=level[0], is_active=True) for level in education_levels}

    # Render the HTML template with context data
    html_string = render_to_string('reports/faculty_education_list.html', {
        'faculty_by_education': faculty_by_education
    })

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="faculty_education_list.pdf"'
    pisa_status = pisa.CreatePDF(
        html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    return response


def generate_faculty_item_status_pdf(request):
    # Get faculty data categorized by education
    item_status_mode = Faculty.STATUS
    faculty_by_status = {level[0]: Faculty.objects.filter(
        item_status=level[0], is_active=True) for level in item_status_mode}

    # Render the HTML template with context data
    html_string = render_to_string('reports/faculty_item_status_list.html', {
        'faculty_by_status': faculty_by_status
    })

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="faculty_item_status.pdf"'
    pisa_status = pisa.CreatePDF(
        html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    return response

# item_status


def get_status_counts(request):
    year = request.GET.get('year_bar')
    query = Faculty.objects.filter(is_active=True)

    if year:
        query = query.filter(date_hired__year=year)

    status_counts = query \
        .annotate(year=ExtractYear('date_hired')) \
        .values('year', 'item_status') \
        .annotate(count=Count('id')) \
        .order_by('year')

    data = {
        'years': [],
        'COS': [],
        'Permanent': [],
        'Vacant': [],
        'JO': []
    }

    for entry in status_counts:
        year = entry['year']
        status = entry['item_status']
        count = entry['count']

        if year not in data['years']:
            data['years'].append(year)
            data['COS'].append(0)
            data['Permanent'].append(0)
            data['Vacant'].append(0)
            data['JO'].append(0)

        index = data['years'].index(year)
        if status == 'COS':
            data['COS'][index] = count
        elif status == 'Permanent':
            data['Permanent'][index] = count
        elif status == 'Vacant':
            data['Vacant'][index] = count
        elif status == 'JO':
            data['JO'][index] = count

    return JsonResponse(data)


def get_gender_counts(request):
    year = request.GET.get('year')
    query = Faculty.objects.filter(is_active=True)

    if year:
        query = query.filter(date_hired__year=year)

    gender_counts = query.values('gender').annotate(
        count=Count('id')).order_by('gender')

    data = {
        'Male': 0,
        'Female': 0
    }

    for entry in gender_counts:
        gender = entry['gender']
        count = entry['count']
        if gender == 'Male':
            data['Male'] = count
        elif gender == 'Female':
            data['Female'] = count

    return JsonResponse(data)


def get_item_status_counts_per_year(request):
    year = request.GET.get('year_line')
    query = Faculty.objects.filter(is_active=True)
    print(year)

    if year:
        query = query.filter(date_hired__year=year)

    status_counts = query \
        .annotate(year=ExtractYear('date_hired')) \
        .values('year', 'item_status') \
        .annotate(count=Count('id')) \
        .order_by('year')

    data = {
        'years': [],
        'COS': [],
        'Permanent': [],
        'Vacant': [],
        'JO': [],
    }

    years = sorted(set(entry['year'] for entry in status_counts))

    for year in years:
        data['years'].append(year)
        data['COS'].append(0)
        data['Permanent'].append(0)
        data['Vacant'].append(0)
        data['JO'].append(0)

    for entry in status_counts:
        year = entry['year']
        status = entry['item_status']
        count = entry['count']
        index = data['years'].index(year)

        if status == 'COS':
            data['COS'][index] = count
        elif status == 'Permanent':
            data['Permanent'][index] = count
        elif status == 'Vacant':
            data['Vacant'][index] = count
        elif status == 'JO':
            data['JO'][index] = count

    return JsonResponse(data)


def get_position_counts(request):
    year = request.GET.get('year_position')
    query = Faculty.objects.filter(is_active=True)

    if year:
        query = query.filter(date_hired__year=year)

    position_counts = query.values('position_id__position_name').annotate(
        count=Count('id')).order_by('position_id__position_name')

    data = {
        'positions': [],
        'counts': []
    }

    for entry in position_counts:
        data['positions'].append(entry['position_id__position_name'])
        data['counts'].append(entry['count'])

    return JsonResponse(data)


def get_item_status_counts(request):
    year = request.GET.get('year_status')
    query = Faculty.objects.filter(is_active=True)

    if year:
        query = query.filter(date_hired__year=year)

    item_status_counts = query.values('item_status').annotate(
        count=Count('id')).order_by('item_status')

    data = {
        'item_status': [],
        'counts': []
    }

    for entry in item_status_counts:
        data['item_status'].append(entry['item_status'])
        data['counts'].append(entry['count'])

    return JsonResponse(data)


def faculty_counts(request):
    male_count = Faculty.objects.filter(gender='Male', is_active=True).count()
    female_count = Faculty.objects.filter(
        gender='Female', is_active=True).count()
    # total_count = Faculty.objects.filter(is_active=True).count()

    context = {
        'male_count': male_count,
        'female_count': female_count,
        'total_count': male_count + female_count,
    }
    return render(request, 'dashboards/gender_counts.html', context)


def faculty_education_counts(request):
    master_count = Faculty.objects.filter(
        education='Master', is_active=True).count()
    doctor_count = Faculty.objects.filter(
        education='Doctor', is_active=True).count()
    # total_count = Faculty.objects.count()

    context = {
        'master_count': master_count,
        'doctor_count': doctor_count,
        'total_count': master_count + doctor_count,
    }
    return render(request, 'dashboards/education_counts.html', context)


def faculty_type_counts(request):
    teaching_count = Faculty.objects.filter(
        employment_type='Teaching', is_active=True).count()
    non_teaching_count = Faculty.objects.filter(
        employment_type='Non-Teaching', is_active=True).count()
    # total_count = Faculty.objects.count()

    context = {
        'teaching_count': teaching_count,
        'non_teaching_count': non_teaching_count,
        'total_count': teaching_count + non_teaching_count,
    }
    return render(request, 'dashboards/type_counts.html', context)


def faculty_status_counts(request):
    jo_count = Faculty.objects.filter(item_status='JO', is_active=True).count()
    cos_count = Faculty.objects.filter(
        item_status='COS', is_active=True).count()
    permanent_count = Faculty.objects.filter(
        item_status='Permanent', is_active=True).count()
    # total_status_count = Faculty.objects.filter(item_status__in=['JO', 'COS', 'Permanent'], is_active=True).count()

    context = {
        'jo_count': jo_count,
        'cos_count': cos_count,
        'permanent_count': permanent_count,
        'jo_cos_count': jo_count + cos_count,
        'total_status_count': jo_count + cos_count + permanent_count,
    }
    return render(request, 'dashboards/faculty_status_counts.html', context)


def faculty_gender_itemstatus_counts(request):
    year = request.GET.get('year_gender_status')
    query = Faculty.objects.filter(is_active=True)
    print(year)
    if year:
        faculty_data = query.filter(
            date_hired__year=year)
    else:
        faculty_data = query

    # year = ExtractYear('date_hired')

    data = faculty_data \
        .annotate(year=ExtractYear('date_hired')) \
        .values('year', 'gender', 'item_status') \
        .annotate(count=Count('id')) \
        .order_by('year', 'gender', 'item_status')

    chart_data = {
        'years': sorted(set(d['year'] for d in data)),
        'male': {'JO': [], 'COS': [], 'Permanent': []},
        'female': {'JO': [], 'COS': [], 'Permanent': []}
    }

    for year in chart_data['years']:
        for status in ['JO', 'COS', 'Permanent']:
            chart_data['male'][status].append(
                next((item['count'] for item in data if item['year'] ==
                     year and item['gender'] == 'Male' and item['item_status'] == status), 0)
            )
            chart_data['female'][status].append(
                next((item['count'] for item in data if item['year'] ==
                     year and item['gender'] == 'Female' and item['item_status'] == status), 0)
            )

    return JsonResponse(chart_data)


def unit_report(request):
    return render(request, 'reports/chart_unit_report.html')


def admin_report_chart(request):
    return render(request, 'reports/chart_admin_report.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# def login(request):
#     return render(request, 'accounts/login.html')


def register(request):
    return render(request, 'accounts/register.html')


@login_required
def management(request):
    return render(request, 'management.html')


def management_content_view(request, menu_item):
    return render(request, f'managements/management_{menu_item.lower().replace(" ", "_")}.html', {'menu_item': menu_item})


@login_required
def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'units/unit_list.html', {'units': units})


def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save()
            render(request, 'units/unit_row.html',
                   {'unit': unit})
    else:
        form = UnitForm()
    return render(request, 'units/unit_form.html', {'form': form})


def unit_update(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        print(form.is_valid())
        if form.is_valid():
            unit = form.save()
            return render(request, 'units/unit_row.html', {'unit': unit})
    else:
        form = UnitForm(instance=unit)
    return render(request, 'units/unit_form.html', {'form': form})


# @require_POST
@require_http_methods(['DELETE'])
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    unit.delete()
    return HttpResponse(status=200)


# department
@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/departments.html', {'departments': departments})


def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            return render(request, 'departments/department-row.html', {'department': department})
    else:
        form = DepartmentForm()
    return render(request, 'departments/department-form.html', {'form': form})


def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            department = form.save()
            return render(request, 'departments/department-row.html', {'department': department})
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/department-form.html', {'form': form})


# @require_POST
@require_http_methods(['DELETE'])
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return HttpResponse(status=200)


# position
@login_required
def position_list(request):
    positions = Position.objects.all()
    return render(request, 'positions/positions.html', {'positions': positions})


def position_create(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save()
            return render(request, 'positions/position-row.html', {'position': position})
    else:
        form = PositionForm()

    return render(request, 'positions/position-form.html', {'form': form})


def position_update(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            position = form.save()
            return render(request, 'positions/position-row.html', {'position': position})
    else:
        form = PositionForm(instance=position)
    return render(request, 'positions/position-form.html', {'form': form})


# @require_POST
@require_http_methods(['DELETE'])
def position_delete(request, pk):
    department = get_object_or_404(Position, pk=pk)
    department.delete()
    return HttpResponse(status=200)


# item
def item_list(request):
    items = Item.objects.all()
    return render(request, 'items/items.html', {'items': items})


def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            return render(request, 'items/item-row.html', {'item': item})
    else:
        form = ItemForm()
    return render(request, 'items/item-form.html', {'form': form})


def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return render(request, 'items/item-row.html', {'item': item})
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/item-form.html', {'form': form})


# @require_POST
@require_http_methods(['DELETE'])
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return HttpResponse(status=204)


# faculty
@login_required
def faculty_list(request):
    faculties = Faculty.objects.all()
    return render(request, 'faculties/faculties.html', {'faculties': faculties})


def faculty_create(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            faculty = form.save()
            return render(request, 'faculties/faculty-row.html', {'faculty': faculty})
    else:
        form = FacultyForm()
    return render(request, 'faculties/faculty-form.html', {'form': form})


def faculty_update(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            faculty = form.save()
            return render(request, 'faculties/faculty-row.html', {'faculty': faculty})
    else:
        form = FacultyForm(instance=faculty)
    return render(request, 'faculties/faculty-form.html', {'form': form})


# @require_POST
@require_http_methods(['DELETE'])
def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    faculty.delete()
    return HttpResponse(status=200)


# authentication / login

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to the home page after login
            return redirect('home:dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home:login')  # Redirect to the login page after logout
