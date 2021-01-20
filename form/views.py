import base64
import datetime
import hashlib
import io
import random
import basehash
from django.contrib import auth
from django.contrib.auth import logout, hashers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
# Create your views here.
# @login_required
# def index(request):
#     return HttpResponse('index')
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from fpdf import FPDF, HTMLMixin
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from form.models import Form, FormFields, Application, UserInfo


# login user
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # if user admin, redirect to index if no just login in system
            if request.user.is_staff:
                return redirect('admin_index')
            return HttpResponse('logged in')
        else:
            return render(request, 'form/login.html', {'message': "Invalid username or password"})
    return render(request, 'form/login.html')


# logout user
def logout_view(request):
    logout(request)
    return redirect('admin_index')


# register user to allow create application, admin user could be registered in django admin Website or by creating
# superuser
def user_registration(request):
    if request.method == 'POST':
        data = request.POST
        if "username" and 'password' and 'first_name' and 'last_name' and 'fathers_name' and 'address' and 'email' in data and len(data['username']) > 0 and len(data['password']) > 0 and len(data['first_name']) > 0 and len(data['last_name']) > 0 and len(data['fathers_name']) > 0 and len(data['address']) > 0 and len(data['email']) > 0:
            username = data['username']
            p = data['password']
            password = make_password(p)
            first_name = data['first_name']
            last_name = data['last_name']
            fathers_name = data['fathers_name']
            address = data['address']
            email = data['email']
            # checking is username used, it should be unique
            check_user = User.objects.filter(username=username)
            if check_user:
                return render(request, 'form/user_registration.html', {'error': "никнейм уже зарегестрирован"})
            else:
                new_user = User(username=username, email=email, password=password)
                new_user.save()
                user = User.objects.get(username=username, email=email, password=password)
                # registering user in table with detail info
                new_user_info = UserInfo(user_id=user.id, first_name=first_name, last_name=last_name, fathers_name=fathers_name, address=address)
                new_user_info.save()
                # login registered user
                user_r = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                return HttpResponse('Hi user {} is registered'.format(user.username))
        else:
            return render(request, 'form/user_registration.html', {'error': "заполните все поля"})
    return render(request, 'form/user_registration.html')


# main page for admin, where info about all forms created
@login_required
def admin_index(request):
    if request.user.is_staff:
        forms = Form.objects.all()
        return render(request, 'form/admin_index.html', {'forms': forms})
    else:
        return HttpResponse("u r not admin")


# admin view for detail of form
@login_required
def form_details(request, id):
    if request.user.is_staff:
        # get application by id
        applications = Application.objects.filter(form_id=id)
        # list for objects with all details of applications
        details = []
        for application in applications:
            # getting user details info
            user = UserInfo.objects.get(user_id=application.user_id)
            user1 = User.objects.get(id=application.user_id)
            # creating detail object for application
            detail = {
                "id": application.id,
                "date": application.date,
                "user_name_details": '{} {} {}'.format(user.first_name, user.last_name, user.fathers_name),
                "address": user.address,
                'email': user1.email,
                "key": application.key,
                "signature": application.signature,
                "link": application.link
            }
            details.append(detail)
        return render(request, 'form/form_details.html', {'details': details})
    else:
        return HttpResponse("u r not admin")


# admin view for creation of form
@login_required
def create_form(request):
    if request.user.is_staff:
        if request.method == 'POST':
            data = request.POST
            # checking do admin feel all data needed to create form
            if 'name' and "form_text" and 'add_number' and "email_subject" in data and len(data['name']) > 0 and \
                    len(data['form_text']) > 0 and int(data['add_number']) > 0 and len(data['email_subject']) > 0:
                name = data['name']
                form_text = data['form_text']
                fields_number = int(data['add_number'])
                email_subject = data['email_subject']
                # list to get all tegs what was created
                fields = []
                # for each created teg in form
                for i in range(fields_number):
                    # checking is each teg created properly
                    if len(data['name{}'.format(i)]) <=0 or len(data['type{}'.format(i)]) <=0 or len(data['tag{}'.format(i)]) <=0:
                        return render(request, 'form/create_form.html', {'error': "Заполните все поля"})
                    else:
                        # details for each teg
                        field = {
                            "name": data['name{}'.format(i)],
                            'type': data['type{}'.format(i)],
                            "tag": data['tag{}'.format(i)]
                        }
                        fields.append(field)
                # getting date
                date = datetime.datetime.now()
                # creating new form
                new_form = Form(user_create_id=request.user.id, title=name, text=form_text, email_subject=email_subject,
                                date_created=date)
                new_form.save()
                form = Form.objects.get(user_create_id=request.user.id, date_created=date)
                # hashing url
                hash_fn = basehash.base36()
                hash_value = hash_fn.hash(form.id)
                link = "https://stormy-mountain-84583.herokuapp.com/application/?application={}".format(hash_value)
                # creating tegs for form
                for field in fields:
                    new_field = FormFields(form_id=form.id, field_title=field['name'], teg=field['tag'],
                                           type=field['type'])
                    new_field.save()
                # updating link for form application
                link = Form.objects.filter(id=form.id).update(link=link)
                return redirect('admin_index')
            else:
                return render(request, 'form/create_form.html', {'error': "Заполните все поля"})
        else:
            return render(request, 'form/create_form.html')
    else:
        return HttpResponse('Not allowed')


# view for user application processing and creation
@login_required
def user_application(request):
    # getting form
    form_id = basehash.base36().unhash(request.GET['application'])
    form_fields = FormFields.objects.filter(form_id=form_id)
    if request.method == 'POST':
        data = request.POST
        # list of all form tegs
        tegs = []
        for field in form_fields:
            # all fields for tegs to be fill
            if field.field_title not in data or len(data[field.field_title]) < 0:
                return render(request, 'form/user_application.html', {"form_fields": form_fields,
                                                                      "error": "заполните все поля"})
            else:
                # object for each teg for processing application and creating user application text
                tag = {
                    "key": field.teg,
                    "value": data[field.field_title]
                }
                tegs.append(tag)
        # getting form text
        form = Form.objects.get(id=form_id)
        text = form.text
        title = form.title
        # processing form text, replacing all tegs with user data
        for teg in tegs:
            text = text.replace('#{}'.format(teg['key']), '{}'.format(teg['value']))
            title = title.replace('#{}'.format(teg['key']), '{}'.format(teg['value']))
        # generating user unique key for signature, checking it to be unique
        number = random.randint(1000, 9999)
        key_exist = Application.objects.filter(key=number)
        if key_exist:
            while key_exist:
                number = random.randint(1000, 9999)
                key_exist = Application.objects.get(key=number)
        else:
            # if key unique registering user application
            key = str(number)
            date = datetime.datetime.now()
            new_application = Application(form_id=form_id, title=title, user_id=request.user.id, text=text, key=key,
                                          date=date)
            new_application.save()
            application = Application.objects.get(key=key)
            # creating and sending email with msg for user (now in terminal)
            message = render_to_string('form/signature_confirmation_email.html', {
                "key": application.key,
                'domain': '127.0.0.1:8000',
                'aid': urlsafe_base64_encode(force_bytes(application.pk))
            })
            mail_subject = form.email_subject
            to_email = request.user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('sign_confirmation', aid=urlsafe_base64_encode(force_bytes(application.pk)))
    return render(request, 'form/user_application.html', {"form_fields": form_fields})


# view for user if he sign application by following link
def sign(request, aid):
    try:
        application_id = force_text(urlsafe_base64_decode(aid))
        application = Application.objects.get(id=application_id)
    except(TypeError, ValueError, OverflowError, Application.DoesNotExist):
        application = None
        return HttpResponse("Invalid link")
    # creating signature sha1
    sign_str = '{}{}'.format(application.text, application.key)
    sign_str_as_bytes = str.encode(sign_str)
    hash_object = hashlib.sha1(sign_str_as_bytes)
    signature = hash_object.hexdigest()
    # updating signature in db
    sing_in = Application.objects.filter(id=application.id).update(signature=signature)
    # creating and updating link for final application view
    link = 'https://stormy-mountain-84583.herokuapp.com/final_preview/{}'.format(aid)
    link_update = Application.objects.filter(id=application_id).update(link=link)
    return redirect('final_preview', aid=aid)


# view for sign application with key
@login_required
def sign_confirmation(request, aid):
    try:
        application_id = force_text(urlsafe_base64_decode(aid))
        application = Application.objects.get(id=application_id)
    except(TypeError, ValueError, OverflowError, Application.DoesNotExist):
        application = None
        return HttpResponse("Invalid application")
    # data for html preview of application
    text = application.text
    t = text.replace('\r', '')
    text_list = t.split('\n')
    if request.method == 'GET':
        return render(request, "form/sign_confirmation.html", {"text": text_list})
    else:
        data = request.POST
        # if user put key
        if 'key' in data and len(data['key']) == 4:
            key = data['key']
            # if key is correct
            if key == application.key:
                # creating signature
                sign_str = '{}{}'.format(application.text, application.key)
                sign_str_as_bytes = str.encode(sign_str)
                hash_object = hashlib.sha1(sign_str_as_bytes)
                signature = hash_object.hexdigest()
                # saving signature and link for application
                sing_in = Application.objects.filter(id=application.id).update(signature=signature)
                link = 'https://stormy-mountain-84583.herokuapp.com/final_preview/{}'.format(aid)
                link_update = Application.objects.filter(id=application_id).update(link=link)
                return redirect('final_preview', aid=aid)
            else:
                return render(request, "form/sign_confirmation.html", {"text": text_list, 'error': "неверный код", 'name': application.title})
        else:
            return render(request, "form/sign_confirmation.html", {"text": text_list, 'error': "неверный код", "name": application.title})


# view for final preview of application
@login_required
def final_preview(request, aid):
    try:
        id_byte = urlsafe_base64_decode(aid)
        application_id = id_byte.decode("utf-8")
        application = Application.objects.get(id=application_id)
    except(TypeError, ValueError, OverflowError, Application.DoesNotExist):
        application = None
        return HttpResponse("Invalid application")
    text = application.text
    t = text.replace('\r', '')
    text_list = t.split('\n')
    return render(request, "form/final_preview.html", {"text": text_list, 'key': application.key,
                                                       "signature": application.signature, "name": application.title,
                                                       'id': application_id})


# view for downloading of application with Canvas
@login_required
def download_application(request, id):
    id = id
    # get application text and process it for downloading
    application = Application.objects.get(id=id)
    text = application.text
    t = text.replace('\r', '')
    text_list = t.split('\n')
    text_list.insert(0, application.title)
    text_list.append(application.signature)
    text_list.append('Ваш уникальный код:')
    text_list.append(application.key)
    # downloading processed aplication to pdf
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    # registering font for cyrillic symbols
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    p.setFont('FreeSans', 10)
    w = 800
    for i in text_list:
        p.drawString(100, w, i.encode('utf-8'))
        w -= 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='{}.pdf'.format(application.title))






