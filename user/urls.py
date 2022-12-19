from django.urls import path, include
from django.conf import settings
from . import views as user_view
from django.conf.urls.static import static
from .views import *
from . import views
from django.contrib.auth import views as auth
from django.contrib import admin
from django.urls import path, include
urlpatterns = [ 
                path('login/', user_view.Login, name ='login'),
                path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
                path('register/', user_view.register, name ='register'),
                #path('uploadImage/',user_view.uploadImage, name='uploadImage'),
                path('index/',user_view.index, name='index' ),
                path('uploadImage/', user_view.uploadImage, name='uploadImage'),
                path('makepredictions/', user_view.makepredictions, name='makepredictions'),
                
                
       ]
       
       
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)