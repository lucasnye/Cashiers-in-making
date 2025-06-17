import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, HexColor
from reportlab.pdfgen import canvas
from io import BytesIO

def dyslexia_friendly_view(request):
    if request.method == 'POST' and request.FILES['pdf']:
        uploaded_file = request.FILES['pdf']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        p.setFillColor(HexColor("#F5F5DC"))
        p.rect(0, 0, width, height, fill=1)

        p.setFont("Helvetica", 14)
        p.setFillColor(black)
        textobject = p.beginText(50, height - 50)
        textobject.setCharSpace(1.5)
        textobject.setWordSpace(5)

        for line in full_text.split("\n"):
            textobject.textLine(line)

        p.drawText(textobject)
        p.showPage()
        p.save()

        buffer.seek(0)
        os.remove(file_path)
        return FileResponse(buffer, as_attachment=True, filename='dyslexia_friendly.pdf')

    return render(request, 'upload.html')
