from django.shortcuts import render

from writing.models import Writing


def entrance(request):
    writings = Writing.objects.all().order_by('-uploaded_time')
    context = {'writings': writings}
    return render(request, 'writing/index.html', context)