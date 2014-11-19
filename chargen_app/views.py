from django.shortcuts import render
from django.template import Context, loader, TemplateDoesNotExist
from chargen_app.forms import DockerfileRequestForm
from django.http import Http404, HttpResponse
from django.core.servers.basehttp import FileWrapper
from dndgen.converter import Converter
from dndgen.fill_pdf import fill_pdf
from dndgen.gen import gen
from fdfgen import forge_fdf
import json
import tempfile
import urllib
import os
import subprocess


def home(request):
    form = DockerfileRequestForm()
    return render(request, "index.html", {'form': form})


def generate(request):
    form = DockerfileRequestForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data["character_sheet"]
        conv = Converter()
        char = conv.convert(data)

        pdf_file = tempfile.NamedTemporaryFile("wb", delete=False)
        pdf_file.close()
        os.unlink(pdf_file.name)
        if request.POST["target"] == "sheet":
            fields = fill_pdf(char)
            fdf = forge_fdf("", fields, [], [], [])
            fdf_file = tempfile.NamedTemporaryFile("wb", delete=False)
            fdf_file.write(fdf)
            fdf_file.close()

            subprocess.call(["pdftk", "dndgen/Interactive_DnD_4.0_Character_Sheet.pdf",
                             "fill_form", fdf_file.name, "output", pdf_file.name, "flatten"])
            os.unlink(fdf_file.name)

            response_file = open(pdf_file.name, 'rb')
            wrapper = FileWrapper(response_file)
            response = HttpResponse(wrapper, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="sheet.pdf"'
            response['Content-Length'] = os.path.getsize(pdf_file.name)
            return response
        if request.POST["target"] == "powers":
            gen(char, pdf_file.name)
            response_file = open(pdf_file.name, 'rb')
            wrapper = FileWrapper(response_file)
            response = HttpResponse(wrapper, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="powers.pdf"'
            response['Content-Length'] = os.path.getsize(pdf_file.name)
            return response
    else:
        return render(request, "index.html", {'form': form})
