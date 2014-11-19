from django.shortcuts import render
from django.template import Context, loader, TemplateDoesNotExist
from chargen_app.forms import DockerfileRequestForm
from django.http import Http404
from dndgen.converter import Converter
from dndgen.fill_pdf import fill_pdf
import json


def home(request):
    form = DockerfileRequestForm()
    return render(request, "index.html", {'form': form})


def generate(request):
    form = DockerfileRequestForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data["character_sheet"]
        conv = Converter()
        char = conv.convert(data)
        fields = fill_pdf(char)
        return render(request, "charfile.html", {'text': json.dumps(fields, indent=2)})
    else:
        return render(request, "index.html", {'form': form})
