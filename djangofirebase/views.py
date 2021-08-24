import pyrebase 
from django.shortcuts import render

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

def getTasks():
    db = firebase.database()
    all_tasks = []
    tasks = db.child("tasks").get()
    
    for task in tasks.each() or []:
        all_tasks.append([task.key(), task.val()])
        
    return all_tasks


def signIn(request):
    return render(request, "signIn.html")

def postSign(request):
    tasks = getTasks()
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    
    try:
        user = auth.sign_in_with_email_and_password(email, passw)
    except:
        message = "Invalid cerediantials"
        return render(request, "signIn.html", {"msg": message})
    
    print(user)
    return render(request, "welcome.html", {"e": email, "t" : tasks})

def postLeave(request):
    try:
        del request.session['token_id']
        auth.signOut()
    except KeyError:
        pass
    
    message = "You are logged out"
    return render(request, "signIn.html", {"msg": message})

def postTask(request):
    tasks = getTasks()
    db = firebase.database()
    user = auth.current_user
    email = user['email']
    contents = request.POST.get('contents')
    data = {"task": contents}
     
    try:
        if contents == "" or len(contents) < 4:
            message = "Your task cannot be empty"
            return render(request, "welcome.html", {"e": email, "t" : tasks, "msg": message})
        else:
            db.child("tasks").push(data, user['idToken'])
    except:
        message = "Not logged in"
        return render(request, "signIn.html", {"msg": message})
    
    return render(request, "welcome.html", {"e": email, "t" : tasks})

def delTask(request):
    tasks = getTasks()
    db = firebase.database()
    user = auth.current_user
    email = user['email']
    task_id = request.POST.get('key')
     
    try:
        db.child("tasks").child(task_id).child('task').remove(user['idToken'])
    except:
        message = "Not logged in"
        return render(request, "signIn.html", {"msg": message})
    
    return render(request, "welcome.html", {"e": email, "t" : tasks})

def editTask(request):
    tasks = getTasks()
    db = firebase.database()
    user = auth.current_user
    email = user['email']
    contents = request.POST.get('contents')
    data = {"task": contents}
     
    try:
        if contents == "" or len(contents) < 4:
            message = "Your task cannot be empty"
            return render(request, "welcome.html", {"e": email, "t" : tasks, "msg": message})
        else:
            db.child("tasks").push(data, user['idToken'])
    except:
        message = "Not logged in"
        return render(request, "signIn.html", {"msg": message})
    
    return render(request, "welcome.html", {"e": email, "t" : tasks})