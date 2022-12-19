import keras
from django.shortcuts import render
from PIL import Image
import numpy as np
import os
from django.core.files.storage import FileSystemStorage
media = 'media'
model = keras.models.load_model(r'C:\Users\mercy\Desktop\Cherry Blossom\cherry_blossom\SavedModel\model.h5')

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from .forms import *
from user.models import uploadImage

#################### index#######################################
def index(request):
	return render(request, 'user/index.html', {'title':'index'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            email = user.email
            ######################### mail system ####################################
            htmly = get_template('user/Email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'your_email@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ##################################################################
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form, 'title':'register here'})


################ login forms###################################################
def Login(request):
	if request.method == 'POST':

		# AuthenticationForm_can_also_be_used__

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {username} !!')
			return redirect('uploadImage')
		else:
			messages.info(request, f'account does not exit please sign in')
	form = AuthenticationForm()
	return render(request, 'user/login.html', {'form':form, 'title':'log in'})
def makepredictions(path):
    print('opening image')
    img = Image.open(path)
    img_d = img.resize((224,224)) # Corrected parentheses
    
    if len(np.array(img_d).shape)<4: # Replaced img.d with img_d
        rgb_img = Image.new("RGB", img_d.size)
        rgb_img.paste(img_d) # Replaced img.d with img_d
    else:
        rgb_img = img_d
    
    rgb_img = np.array(rgb_img, dtype = np.float64)
    rgb_img = rgb_img.reshape(1,224,224,3) # Corrected shape from (1,244,244,3) to (1,224,224,3)
    print('loading model')
    model = keras.models.load_model(r"C:\Users\mercy\Desktop\Cherry Blossom\cherry_blossom\SavedModel\model.h5")
    print('model')
    print(model)
    predictions = model.predict(rgb_img)
    print('prediction')
    print(predictions)
    a = int(np.argmax(predictions))
    if a == 0:
        result = " Result : Presence of PCOS Detected"
    else :
        result = "Result : No PCOS Detected "
    return result

def uploadImage(request):
    if request.method == "POST" and 'image' in request.FILES:
        name = request.POST.get('name')
        f = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(f.name, f)
        file_url = fss.url(file)
        file_path = fss.open(f.name)
        print(file_path)
        print(f'file_url: {file_url}')
        predictions = makepredictions(os.path.join(media, file))
        messages.success(request, 'Image uploaded and predictions made successfully!')
        return render(request, 'user/uploadImage.html',{'pred':predictions, 'file_url': file_url})
            
    else:
        return render(request, 'user/uploadImage.html')
        print(request.files)

#   
# def uploadImage(request):
#     if request.method == "GET":
#         return render(request, 'user/uploadImage.html')
#     elif request.method == "POST":
#         if 'uploadImage' not in request.FILES:
#             err = 'No Image Selected'
#             return render(request, 'user/uploadImage.html', {'err':err})
#         upload_image = request.FILES.get('uploadImage', None)
#         if not upload_image:
#             err = 'No file selected'
#             return render(request, 'user/uploadImage.html',{'err':err})
#         fss = FileSystemStorage()
#         file = fss.save(upload_image.name, upload_image)
#         file_url = fss.url(file)
#         predictions = makepredictions(os.path.join(media, file))
#         return render(request, 'user/uploadImage.html',{'pred':predictions, 'file_url': file_url})




# def uploadImage(request):
#   if request.method == 'POST':
#     image = request.FILES['image']
#     # Use the image to make a prediction using the CNN model
#     prediction = model.predict(image)
#     return HttpResponse(prediction)
#   else:
#     return render(request, 'uploadImage.html')
