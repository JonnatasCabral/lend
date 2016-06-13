from django.shortcuts import render


def index(request):
    return render(request, template_name='index.html')

def code_editor(request):
    return render(request, template_name='code_editor.html')
