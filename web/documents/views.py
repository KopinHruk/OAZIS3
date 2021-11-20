from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import forms


class UploadForm(forms.Form):
    title = forms.CharField(max_length=50,  widget=forms.TextInput(attrs={'class': "form-control"}))
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': "form-control", 'multiple': True}))


def upload_view(request):
    template = loader.get_template('documents/upload.html')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            process_documents(request.FILES['file'])
            return HttpResponseRedirect('/results/')
    #else:
    form = UploadForm()
    return HttpResponse(template.render({'form': form}, request))


def process_documents(documents):
    for document in documents:
        pass



def result_view(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('documents/results.html')
    context = {
     #   'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))