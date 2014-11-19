from django.shortcuts import render
from django.template import Context, loader, TemplateDoesNotExist
from chargen_app.forms import DockerfileRequestForm
from django.http import Http404


def home(request):
    if request.method == 'POST':
        form = DockerfileRequestForm(request.POST)
        # if form.is_valid():
        #     template = loader.get_template("docker/centos6.dockerfile")
        #     dd = template.render(Context(form.cleaned_data))
        #     return render(request, "dockerfile.html", {'dockerfile': dd})
    else:
        form = DockerfileRequestForm()

    return render(request, "index.html", {'form': form})


# def generate(request):
#     form = DockerfileRequestForm(request.GET)
#     if form.is_valid():
#         os = form.cleaned_data["os"]
#         try:
#             template = loader.get_template("docker/{}.dockerfile".format(os))
#         except TemplateDoesNotExist:
#             raise Http404('Template for "{}" does not exists'.format(os))
#         dd = template.render(Context(form.cleaned_data))
#         return render(request, "dockerfile.html", {"dockerfile": dd})
#     else:
#         return render(request, "index.html", {'form': form})
