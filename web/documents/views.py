from django.http import HttpResponse, HttpResponseRedirect
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
            config = {
                'type': form.cleaned_data.get("type"),
                'number_of_sentences': form.cleaned_data.get('num_sen'),
                'number_of_key_words': form.cleaned_data.get('num_keys')

            }
            return process_documents(request, request.FILES.getlist('file'), config)
            # return HttpResponseRedirect('/results/')

    form = UploadForm()
    return HttpResponse(template.render({'form': form}, request))


def process_documents(request, documents, config):
    documents = [document.file.read().decode('utf-8') for document in documents]
    output = process(documents, config)

    template = loader.get_template('documents/results.html')
    context = {
        'output': output,
    }
    return HttpResponse(template.render(context, request))


def result_view(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('documents/results.html')
    context = {
        'output': None,
    }
    return HttpResponse(template.render(context, request))