import io
import json
import os

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django import forms

from summarizers.processor import process


class UploadForm(forms.Form):
    marcas = (
        ('ml', 'ML'),
        ('classic', 'Classic')
    )

    type = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': "form-check-label"}), choices=marcas)
    num_sen = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control", 'value': 10}))
    num_keys = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control", 'value': 10}))

    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': "form-control", 'multiple': True}))


def upload_view(request):
    template = loader.get_template('documents/upload.html')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            type = form.cleaned_data.get("type")
            config = {
                'type': type,
                'number_of_sentences': form.cleaned_data.get('num_sen'),
                'number_of_key_words': form.cleaned_data.get('num_keys'),
                'header1': 'Abstract' if type == 'ml' else 'Classic',
                'header2': 'Extract' if type == 'ml' else 'Key Words',

            }
            process_documents(request.FILES.getlist('file'), config)
            return HttpResponseRedirect('/results/')

    form = UploadForm()
    return HttpResponse(template.render({'form': form}, request))


def process_documents(documents, config):
    documents = [document.file.read().decode('utf-8') for document in documents]
    output = process(documents, config)

    with open('temp.json', 'w') as outfile:
        json.dump({'output': output, 'config': config}, outfile)


def result_view(request):
    with open('temp.json') as json_file:
        data = json.load(json_file)
    output = data['output']
    config = data['config']

    paginator = Paginator(output, 1)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = loader.get_template('documents/results.html')

    context = {'page_obj': page_obj,
               'header1': config['header1'],
               'header2': config['header2'],
               }
    return HttpResponse(template.render(context, request))


def download_files(request):
    with open('temp.json') as json_file:
        data = json.load(json_file)
    output = data['output']
    config = data['config']


    f = io.StringIO(config['header1'] + "\n" + output[0][1] + "\n" + config['header2'] + "\n" + output[0][2])
    response = HttpResponse(f, content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename=results.txt'
    return response
