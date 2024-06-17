from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

#create your views.here

@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    projects = Projects.objects.all()
    users = CustomUser.objects.all()
    task = Task.objects.all()
    tasks_completed = Task.objects.filter(status='completed')
    tasks_pending = Task.objects.filter(status='pending')
    tasks_inprogress = Task.objects.filter(status='inprogress')
    tasks_testing = Task.objects.filter(status='testing')

    return render(request, 'index.html', {
        'tasks_completed': tasks_completed,
        'tasks_pending': tasks_pending,
        'tasks_inprogress': tasks_inprogress,
        'tasks_testing': tasks_testing,
        'task':task,
        'projects': projects, 
        'users': users
    })


@login_required
def get_project_data(request, project_id):
    try:
        project = Projects.objects.get(id=project_id)
        tasks = Task.objects.filter(projects=project)

        # Prepare a list of task data
        tasks_data = []
        for task in tasks:
            assigned_by = {
                'username': task.assigned_by.username,
            }

            assigned_to = {
                'username': task.assigned_to.username,
            }

            task_data = {
                'task_id': task.id,
                'description':task.description,
                'project_name': task.name,
                'status': task.status,
                'assigned_by': assigned_by,
                'assigned_to': assigned_to,
            }
            tasks_data.append(task_data)

        
        return JsonResponse({'tasks': tasks_data})
    except Projects.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

@login_required
def add_task(request):
    projects = Projects.objects.all()
    users = CustomUser.objects.all()
    if request.user.is_authenticated and request.user.role in ['admin', 'manager']:
        if request.method == 'GET':
            projects_id = request.GET.get('project_Id')
            request.session['projects_id'] = projects_id 
            print(projects_id)
            
        if request.method == 'POST':
            projects_id = request.session.get('projects_id')
            name = request.POST.get('name')
            status = request.POST.get('status')
            assigned_to_id = request.POST.get('assigned_to')
            assigned_by_id = request.POST.get('assigned_by')
            
            try:
                projects = Projects.objects.get(id=projects_id)
                assigned_to = CustomUser.objects.get(id=assigned_to_id)
                assigned_by = CustomUser.objects.get(id=assigned_by_id)
            except (Projects.DoesNotExist, CustomUser.DoesNotExist):
                projects = None
                assigned_to = None 
                assigned_by = None
                
            task = Task.objects.create(
                projects=projects,
                name=name,
                status=status,
                assigned_to=assigned_to,
                assigned_by=assigned_by,
            )
            task.save()
            del request.session['projects_id']
            
            return JsonResponse({'status': 'task is added '})

        else:
            return render(request, 'index.html', {'projects': projects, 'users': users})
    else:
        return redirect('index')
    
@login_required
def add_project(request):
    if request.user.is_authenticated and request.user.role in ['admin', 'manager']:
        if request.method == 'POST':
            project_name = request.POST.get('project_name')
            project = Projects.objects.create(
                projects=project_name
            )
            project.save()
            return redirect('add_task')
        else:
            return render(request, 'projectform.html')
    else:
        # Redirect non-authenticated or non-admin/manager users
        return redirect('index')

@login_required
def update_task(request):
    if request.method == 'GET':
        task_id= request.GET.get('taskID')
        request.session['task_id'] = task_id 
        print(task_id)
        try:
            task = Task.objects.get(id=task_id)
            task_data = {
                "name": task.name,
                "description":task.description
            }
            response_data = {'data':task_data}
                
            return JsonResponse(response_data)
        
        except Task.DoesNotExist:
            pass
        
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        task_id = request.session.get('task_id')
        task = Task.objects.get(id=task_id)
        print(task)
        task.name = name
        task.description = description
        task.save()
        
        return JsonResponse({'status': 'task is updated '})   
        
    return render(request, 'index.html')

@login_required
def update_status(request, task_id, status):
    print(request.user,"User")
    if request.user.role in ['admin', 'manager','tester','developer']:
        if request.method == 'POST':
            try:
                task = Task.objects.get(id=task_id)
                task.status = status
                task.save()

                return JsonResponse({'success': True, 'message': 'Task updated successfully'})
            except Task.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Task not found'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})



@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)

    # Check if the user is allowed to delete the task
    if request.user.is_authenticated and request.user.role in ['admin', 'manager']:
        task.delete()
        return redirect('index')
    else:
        # Redirect non-authenticated or non-admin/manager users
        return redirect('index')

def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Username already exists'})
        
        CustomUser.objects.create_user(username=username, password=password)
        return redirect('login') 
    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request ,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request,"login.html",{'error_message': 'Invalid Credentials.'})
    return render(request,"login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect('login') 

