import pyrebase 
from django.shortcuts import render, redirect
import time

config = {
        "apiKey": "",
        "authDomain": "",
        "databaseURL": "",
        "projectId": "",
        "storageBucket": "",
        "messagingSenderId": "",
        "appId": "",
        "measurementId": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def getTasks():
    all_tasks = []
    tasks = db.child("tasks").get()
    
    for task in tasks.each() or []:
        all_tasks.append([task.key(), task.val()])
        
    return all_tasks


def loadHome(request):
    try:
        request.session['userAccount']
    except KeyError:
        return redirect('/')
    
    tasks = getTasks()
    user = auth.current_user
    email = user['email']
    return render(request, "welcome.html", {"e": email, "t" : tasks})

def signIn(request):
    try:
        request.session['userAccount']
    except KeyError:
        return render(request, "signIn.html")
    
    return redirect('/home')
    

def postSign(request):
    tasks = getTasks()
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    
    try:
        user = auth.sign_in_with_email_and_password(email, passw)
    except:
        message = "Invalid credentials"
        return render(request, "signIn.html", {"msg": message})
    
    user = auth.refresh(user['refreshToken'])
    print(user)
    request.session['userAccount'] = user
    render(request, "welcome.html", {"e": email, "t" : tasks})
    return redirect('/home/')

def logOut(request):
    request.session.flush()
    request.session.modified = True
    return redirect('/')

def postTask(request):
    try:
        request.session['userAccount']
    except KeyError:
        return redirect('/')
    
    tasks = getTasks()
    user = auth.current_user
    email = user['email']
    contents = request.POST.get('contents')
    data = {"task": contents}
     
    if contents == "" or len(contents) < 4:
        message = "Your task cannot be empty"
        render(request, "welcome.html", {"e": email, "t" : tasks, "msg": message})
    else:
        db.child("tasks").push(data, user['idToken'])
        tasks = getTasks()
    
    render(request, "welcome.html", {"e": email, "t" : tasks})
    return redirect('/home/')

def delTask(request):
    try:
        request.session['userAccount']
    except KeyError:
        return redirect('/')
    
    tasks = getTasks()
    user = auth.current_user
    email = user['email']
    task_id = request.POST.get('key')
    
    db.child("tasks").child(task_id).child('task').remove(user['idToken'])
    tasks = getTasks()
    
    render(request, "welcome.html", {"e": email, "t" : tasks})
    return redirect('/home/')

def editTask(request):
    try:
        request.session['userAccount']
    except KeyError:
        return redirect('/')
    
    tasks = getTasks()
    user = auth.current_user
    email = user['email']
    task_id = request.POST.get('key')

    return render(request, "welcome.html", {"e": email, "t" : tasks, "tid": task_id})
    
    
def saveTask(request):
    try:
        request.session['userAccount']
    except KeyError:
        return redirect('/')
    
    tasks = getTasks()
    user = auth.current_user
    email = user['email']
    task_id = request.POST.get('key')
    contents = request.POST.get('contents')
    
    db.child("tasks").child(task_id).update({"task": contents}, user['idToken'])
    tasks = getTasks()
    
    render(request, "welcome.html", {"e": email, "t" : tasks})
    return redirect('/home/')