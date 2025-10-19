# from django.shortcuts import render,redirect,HttpResponse
# from django.contrib.auth.models import User
# from django.contrib import messages

# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
# from .utils import TokenGenerator,generate_token
# from django.utils.encoding import force_bytes
# from django.utils.encoding import force_str
# from django.utils.encoding import DjangoUnicodeDecodeError
# from django.views.generic import View
# from django.core.mail import EmailMessage
# from django.conf import settings

# from django.contrib.auth import authenticate,login,logout

# def signup(request):
#     if request.method == "POST" :
#         email = request.POST['email']
#         password = request.POST['pass1']
#         confirmpassword = request.POST['pass2']

#         if password != confirmpassword :
#             messages.warning(request,"Password is not Matching")
#             return render(request,'signup.html')
        
#         try:
#             if User.objects.get(username = email):
#                 messages.warning(request,"Username already exits")
#                 return render(request,'signup.html')


#         except Exception as identifier:
#             pass
#         user = User.objects.create_user(email,email,password)
#         user.is_active = False
#         user.save()
#         email_subject = "Activate Your Account"
#         message = render_to_string('activate.html',{
#             'user':user,
#             'domain':'127.0.0.1:8000',
#             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#             'token':generate_token.make_token(user)
#         })
#         #search email send in django for below code
#         #format == email_message=EmailMessage("Subject here", "Here is the message.","from@example.com",["to@example.com"],fail_silently=False,)
#         email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
#         email_message.send()
#         messages.success(request,"Activate Your Account by clicking the link in your email")
#         return redirect('/auth/login')
#     return render(request,"signup.html")






# class ActivateAccountView(View):
#     def get(self,request,uidb64,token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except Exception as identifier:
#             user = None
#         if user is not None and generate_token.check_token(user,token):
#             user.is_active = True
#             user.save()
#             messages.info(request,"Account Activated Successfully")
#             return redirect('/auth/login')
#         return render(request,'activatefail.html')





# def handlelogin(request):
#     if request.method == "POST":
#         username = request.POST['email']
#         userpassword = request.POST['pass1']
#         myuser = authenticate(username=username,password=userpassword)

#         if myuser is not None:
#             login(request,myuser)
#             messages.success(request,"Logic Successful")
#             return redirect('/')
#             #return render(request,"index.html")   we can also write in this format (redirect and render are similar )
#             #redirect takes url path and render take direct file path name
#         else:
#             messages.error(request,"Invalid Credentials")
#             return redirect('/auth/login')

#     return render(request,"login.html")





# def handlelogout(request):
#     logout(request)
#     messages.info(request,"Logout Successfully")
#     return redirect('/auth/login')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import View
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .utils import TokenGenerator, generate_token

# Signup view
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass1']
        confirmpassword = request.POST['pass2']

        if password != confirmpassword:
            messages.warning(request, "Passwords do not match")
            return render(request, 'signup.html')

        if User.objects.filter(username=email).exists():
            messages.warning(request, "Username already exists")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False
        user.save()

        email_subject = "Activate Your Account"
        message = render_to_string('activate.html', {
            'user': user,
            'domain': '127.0.0.1:8000',  # Replace with deployed domain
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })

        try:
            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
            email_message.send()
            messages.success(request, "Activate your account via email link")
        except Exception as e:
            messages.error(request, f"Email sending failed: {e}")
            user.delete()  # optional: delete inactive user if email fails
            return render(request, 'signup.html')

        return redirect('/auth/login')

    return render(request, "signup.html")


# Activate Account View
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully")
            return redirect('/auth/login')

        messages.error(request, "Activation link is invalid!")
        return render(request, 'activatefail.html')


# Login
def handlelogin(request):
    if request.method == "POST":
        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username, password=userpassword)

        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login successful")
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/auth/login')

    return render(request, "login.html")


# Logout
def handlelogout(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('/auth/login')
