from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Todo

# Main routes
def index(request):
    
    if request.method == "GET":
        todos = Todo.objects.all().order_by('text')
        users = User.objects.all()
        # to-do: get user and todo info from db
        return render(request, 'todoapp/index.html', {'todos': todos, 'users': users})
    elif request.method == "POST":
        try: 
            userid = request.POST['userid']
        except(KeyError):
            return render(request, 'todoapp/index.html', {'error': 'You must select an owner'})
        else:
            new_todo = Todo()
            new_todo.text = request.post['text']
            new_todo.user = User.objects.get(pk=userid)
            new_todo.save()
            return redirect('index')

def delete(request, todo_id):
    item = Todo.objects.get(id=todo_id)
    item.delete()
    return redirect('index')
    # Alternative syntax for delete
    # Todo.objects.filter(id=todo.id).delete()

def done(request, todo_id):
    item = Todo.objects.get(id=todo_id)
    item.is_complete = True
    item.save()
    return redirect('index')

# Auth-related routes
# this is where we'll connect our auth
def signup(request):
    if request.method == 'GET':
        
        return render(request, 'todoapp/signup.html', {'todos': todos, 'users': users})
    elif request.method == 'POST':
        print("route reached")
        username = request.POST['username']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        try:
            user = User.objects.create_user(username=username, password=password, first_name=firstname)
            if user is not None:
                return login(request)
        except: 
            return render(request, 'todoapp/signup.html', {'Error': 'Username already exists'})
        # return HttpResponse('Posted to signup')

def login(request):
    # return HttpResponse('login')
    if request.method == 'GET':
        # return HttpResponse('Posted to signup')
        return render(request, 'todoapp/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, 'todoapp/login.html', {'error': 'Invalid Credentials'})

def logout(request):
    auth.logout(request)
    return redirect('index')
    # return HttpResponse('logout')
