from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView

from writing.writing_forms import WritingForm
from writing.models import Writing, Tag


class WritingView(DetailView):
    model = Writing
    context_object_name = 'writing'


class WritingListView(ListView):
    model = Writing
    ordering = ['-uploaded_time']
    paginate_by = 5


class EntranceView(TemplateView):
    template_name = 'writing/writing_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class WriteView(TemplateView):
    template_name = 'writing/write_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'write_form': WritingForm()})

    def post(self, request):
        request_post = request.POST
        input_tags = request_post['tags'].split(',')
        duplicated_tags = list(Tag.objects.filter(name__in=input_tags))
        Tag.objects.bulk_create([tag for tag in input_tags if not tag in set(map(lambda tag: tag.name, duplicated_tags))])

        writing = Writing(title=request_post['title'], contents=request_post['contents'])
        writing.save()
        for tag_query_set in Tag.objects.filter(name__in=input_tags):
            writing.tags.add(tag_query_set)
        return HttpResponseRedirect(reverse('writing:'))
