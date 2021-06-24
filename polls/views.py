from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.core import serializers


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for obj in serializers.deserialize("json", request.FILES['file']):
                obj.save()
            return HttpResponseRedirect('../')
    else:
        form = UploadFileForm()
    return render(request, 'post.html', {'form': form})

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
