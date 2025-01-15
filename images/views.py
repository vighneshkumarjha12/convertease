from django.shortcuts import render, HttpResponse
from PIL import Image
import img2pdf
import io
from django.contrib.auth import logout, authenticate, login 
from datetime import datetime
from images.models import Contact
from django.contrib import messages
def home(request):
    return render(request, 'home.html')


def services(request):
    return render(request, 'service.html')
def imgtopdf(request):
    """Convert multiple images to PDF format."""
    if request.method == 'POST':  # Process only if the request is a POST
        try:
            files = request.FILES.getlist('img')  # Get the list of uploaded files
            if not files:  # Check if no files are uploaded
                return HttpResponse("No files selected for conversion.")
            
            pdf = img2pdf.convert([file.read() for file in files])  # Convert all files to PDF
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="converted.pdf"'
            return response
        except Exception as e:
            return HttpResponse(f"Error: {e}")

    # For GET requests, just render the imgtopdf page
    return render(request, 'imgtopdf.html')



def jpgtopng(request):
    """Convert multiple JPGs to PNG format."""
    if request.method == 'POST':
        try:
            files = request.FILES.getlist('img')  # Get the list of uploaded files
            response = HttpResponse(content_type="image/png")
            for img in files:
                im = Image.open(img)
                # Convert each image to PNG and write it to the response
                im.save(response, "PNG")
            response['Content-Disposition'] = 'attachment; filename="converted.png"'
            return response
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    return render(request, 'jpgtopng.html')

def pngtojpg(request):
    """Convert multiple PNGs to JPG format."""
    if request.method == 'POST':
        try:
            files = request.FILES.getlist('img')  # Get the list of uploaded files
            response = HttpResponse(content_type="image/jpeg")
            for img in files:
                im = Image.open(img)
                # Convert to RGB if necessary
                if im.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", im.size, (255, 255, 255))
                    background.paste(im, mask=im.split()[3])  # Using alpha channel
                    im = background
                else:
                    im = im.convert('RGB')
                im.save(response, "JPEG")
            response['Content-Disposition'] = 'attachment; filename="converted.jpg"'
            return response
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    return render(request, 'pngtojpg.html')

def webptopng(request):
    """Convert multiple WEBP images to PNG format."""
    if request.method == 'POST':
        try:
            files = request.FILES.getlist('img')  # Get the list of uploaded files
            response = HttpResponse(content_type="image/png")
            for img in files:
                im = Image.open(img)
                im.save(response, "PNG")
            response['Content-Disposition'] = 'attachment; filename="converted.png"'
            return response
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    return render(request, 'webptopng.html')

def pngtowebp(request):
    """Convert multiple PNG images to WEBP format."""
    if request.method == 'POST':
        try:
            files = request.FILES.getlist('img')  # Get the list of uploaded files
            response = HttpResponse(content_type="image/webp")
            for img in files:
                im = Image.open(img)
                im.save(response, "WEBP")
            response['Content-Disposition'] = 'attachment; filename="converted.webp"'
            return response
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    return render(request, 'pngtowebp.html')

def htu(request):
    return render(request, 'htu.html')
def services(request):
    return render(request, 'services.html')


def blogs(request):
    return render(request, 'blogs.html')



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date = datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'contact.html')
 

