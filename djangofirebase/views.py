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

def signIn(request):
    return render(request, "signIn.html")

def postSign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = auth.sign_in_with_email_and_password(email, passw)
    except:
        message = "Invalid cerediantials"
        return render(request, "signIn.html", {"msg": message})
    
    print(user)
    return render(request, "welcome.html", {"e": email})

def postTask(request):
    email = request.POST.get('email')
    contents = request.POST.get('contents')
    
    db = firebase.database()
    data = {"task": contents}
      
    try:
        db.child("tasks").push(data) 
    except:
        message = "Conexion error"
        return render(request, "signIn.html", {"msg": message})
        
    return render(request, "welcome.html", {"e": email})
