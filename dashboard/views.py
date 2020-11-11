

# Create your views here.

from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Contact
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def index(request):
    return render(request,'dashboard/index.html')
    
def about(request):
    return render(request, 'dashboard/about.html')

def analyze(request):
    # Get the text
    djtext = request.POST.get('text', 'default')
    removepunc=request.POST.get('removepunc','off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    charcount= request.POST.get('charcount','off')

    if removepunc == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char
        params = {'purpose': 'Removed Punctuations', 'analyzed_text': analyzed}
        djtext = analyzed
    

    if(fullcaps=="on"):
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char.upper()

        params = {'purpose': 'Changed to Uppercase', 'analyzed_text': analyzed}
        djtext = analyzed
        

    if(extraspaceremover=="on"):
        analyzed = ""
        for index, char in enumerate(djtext):
            if not(djtext[index] == " " and djtext[index+1]==" "):
                analyzed = analyzed + char

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        djtext = analyzed
        

    if (newlineremover == "on"):
        analyzed = ""
        for char in djtext:
            if char != "\n" and char!="\r":
                analyzed = analyzed + char
            else:
                print("no")
        print("pre", analyzed)
        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        djtext = analyzed
        
    
    if (charcount == 'on'):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        analysed = ""
        count = 0
        for char in djtext:
            if char not in punctuations and char != ' ' and char != '\n':
                count+=1
        analysed = count
        params = {'purpose':'Character Counter', 'analyzed_text':f'{djtext} \nNumber of characters are: {analysed}'}
    if (charcount == 'off') and (newlineremover == "off") and (extraspaceremover=="off") and (fullcaps=="off") and (removepunc == "off"):
        return HttpResponse('<h1>Error!!! Please choose any Option </h1> <br> <h1><a href="/"> Back to home</a></h1>')
    
    
    return render(request, 'dashboard/analyze.html', params)

def contact(request):
    if request.method=='POST':

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<0:
            messages.error(request, "PLease fill the details correctly.")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            messages.success(request, "Your form has been successfully sent.")
            contact.save()
            
    return render(request, 'dashboard/contact.html')

# Handle Signup Page
def handleSignup(request):
    # Get the post parameters
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #Check for errorneous inputs
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('/')
        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers")
            return redirect('/')
        if (pass1 != pass2):
            messages.error(request, "Password do not match")
            return redirect('/')

        #Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.fname = fname
        myuser.lname = lname
        myuser.save()
        messages.success(request, "Your account has been created successfully.")
        return redirect('/')        

    else:
        return HttpResponse("404 - Page not found")

# Handle Login Page
def handleLogin(request):
    if request.method == 'POST':
        #Get the post parameters
        
        loginemail = request.POST['loginemail']
        loginpassword = request.POST['loginpassword']
        username = User.objects.get(email=loginemail.lower()).username
        user = authenticate(username = username, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/')

    return HttpResponse("404 - Page not found")

# Handle Logout Page
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('/')
