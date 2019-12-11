from django.shortcuts import render

from writing.models import Writing


def entrance(request):
    writings = Writing.objects.all().order_by('-uploaded_time')
    context = {'writings': writings}
    return render(request, 'writing/index.html', context)


def write_form(request):
    a = request
    print('a : ' , a.path)
    return render(request, 'writing/write_form.html')


def write(request):
    writing = Writing(title=request.title, contents=request.contents)
    return None