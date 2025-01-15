from django.urls import path
from . import views

urlpatterns = [
    path('', views.imgtopdf, name='home'),  # Set 'imgtopdf' as the home page
    path('jpgtopng', views.jpgtopng, name='jpgtopng'),
    path('pngtojpg', views.pngtojpg, name='pngtojpg'),
    path('webptopng', views.webptopng, name='webptopng'),
    path('pngtowebp', views.pngtowebp, name='pngtowebp'),
    path('htu', views.htu, name='htu'),
    path('services', views.services, name='services'),
    path('contact', views.contact, name='contact'),
    path('blogs', views.blogs, name='blogs'),
    
]
