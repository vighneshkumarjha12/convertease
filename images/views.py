from django.shortcuts import render, HttpResponse
from PIL import Image
import img2pdf
import io
import os
from django.contrib.auth import logout, authenticate, login 
from datetime import datetime
from images.models import Contact
from django.contrib import messages
from django.http import HttpResponse
import pdfplumber
from docx import Document
from pptx import Presentation
from pptx.util import Inches
from pdf2image import convert_from_bytes  # Library to convert PDF to images (install with pip install pdf2image)
from pdf2image import convert_from_path
import fitz  # PyMuPDF
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def home(request):
    return render(request, 'home.html')
def pdf_to_ppt(request):
    """Convert a PDF file to a PowerPoint presentation, preserving text and images."""
    if request.method == 'POST':
        try:
            # Get the uploaded PDF file
            pdf_file = request.FILES.get('pdf_file')
            if not pdf_file:
                return HttpResponse("No file uploaded.", status=400)

            # Read the PDF file
            pdf_data = pdf_file.read()
            pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

            # Create a new PowerPoint presentation
            presentation = Presentation()

            # Loop through each page in the PDF
            for page_number in range(len(pdf_document)):
                page = pdf_document[page_number]

                # Extract text and images from the page
                text = page.get_text("text")  # Extract text as plain text
                images = page.get_images(full=True)  # Get all images

                # Add a new slide
                slide = presentation.slides.add_slide(presentation.slide_layouts[5])  # Blank slide layout

                # Add text to the slide
                if text.strip():
                    textbox = slide.shapes.add_textbox(Pt(10), Pt(10), Pt(960), Pt(540))
                    text_frame = textbox.text_frame
                    p = text_frame.add_paragraph()
                    p.text = text
                    p.font.size = Pt(14)
                    p.font.color.rgb = RGBColor(0, 0, 0)  # Black text
                    p.alignment = PP_ALIGN.LEFT

                # Add images to the slide
                for img_index, img in enumerate(images):
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]  # Image extension (e.g., 'png', 'jpeg')

                    # Save the image temporarily
                    image_filename = f"temp_image_{page_number}_{img_index}.{image_ext}"
                    with open(image_filename, "wb") as img_file:
                        img_file.write(image_bytes)

                    # Add the image to the slide
                    slide.shapes.add_picture(image_filename, Pt(50), Pt(150), Pt(400), Pt(300))

            # Prepare the PowerPoint file as a response
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
            response['Content-Disposition'] = 'attachment; filename="converted.pptx"'
            presentation.save(response)
            return response

        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)

    return render(request, 'pdf_to_ppt.html')




def pdf_to_word(request):
    """Convert a PDF file to a Word document."""
    if request.method == 'POST':
        try:
            pdf_file = request.FILES.get('pdf_file')  # Get the uploaded PDF file
            if not pdf_file:
                return HttpResponse("No file uploaded.", status=400)

            # Extract text from the PDF using pdfplumber
            pdf_text = []
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    pdf_text.append(page.extract_text())

            # Create a Word document using python-docx
            doc = Document()
            doc.add_heading("PDF to Word Conversion", level=1)
            for page_num, page_text in enumerate(pdf_text, start=1):
                doc.add_heading(f"Page {page_num}", level=2)
                doc.add_paragraph(page_text)

            # Prepare the Word file as a response
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename="converted.docx"'
            doc.save(response)
            return response

        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)

    return render(request, 'pdf_to_word.html')

def services(request):
    return render(request, 'service.html')

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'about.html')

def career(request):
    return render(request, 'career.html')

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
 

