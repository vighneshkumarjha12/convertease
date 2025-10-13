from django.urls import path
from . import views

urlpatterns =  [
     path('', views.imgtopdf, name='home'),  # Set 'imgtopdf' as the home page
    path('jpgtopng', views.jpgtopng, name='jpgtopng'),
    path('pngtojpg', views.pngtojpg, name='pngtojpg'),
    path('webptopng', views.webptopng, name='webptopng'),
    path('pngtowebp', views.pngtowebp, name='pngtowebp'),
    path('htu', views.htu, name='htu'),
    path('services', views.services, name='services'),
    path('contact', views.contact_view, name='contact'),
    path('blogs', views.blogs, name='blogs'),
    path('faq', views.faq, name='faq'),
    path('about', views.about, name='about'),
    path('career', views.career, name='career'),
    path('pdf_to_word', views.pdf_to_word, name='pdf_to_word'),
    path('pdf_to_ppt', views.pdf_to_ppt, name='pdf_to_ppt'),
    path('remove_background_view', views.remove_background_view, name='remove_background'),
    path('pdf_to_excel', views.pdf_to_excel, name='pdf_to_excel'),
    path('add-background', views.add_background, name='add_background'),
 

]
      
   



