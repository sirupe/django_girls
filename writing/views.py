from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from writing.writing_forms import WritingForm
from writing.models import Writing, Tag


def entrance(request):
    writings = Writing.objects.all().order_by('-uploaded_time')
    context = {'writings': writings}
    return render(request, 'writing/index.html', context)


def write_form(request):
    context = {'write_form': WritingForm()}
    return render(request, 'writing/write_form.html', context)


def write(request):
    request_post_params = request.POST

    # 태그를 각각 분리한다(',')
    tags = request_post_params['tags'].split(',')
    # 분리한 태그들을 저장한다. 이 때 기존에 존재하는 태그는 insert 하지 않는다.
    #  -1. 입력된 태그와 중복되는 태그가 기존 테이블에 있는지 조회
    duplicated_tags = list(Tag.objects.filter(name__in=tags))
    duplicated_tag_names = set(map(lambda tag: tag.name, duplicated_tags))
    #  -2. -1 에서 조회된 데이터를 tags 에서 제외
    tags_set = []
    for tag in tags:
        if not tag in duplicated_tag_names:
            tags_set.append(Tag(name=tag))
    #  -3. tags 저장
    Tag.objects.bulk_create(tags_set)
    tags_query_set = Tag.objects.filter(name__in=tags)
    # 글을 저장한다.
    writing = Writing(title=request_post_params['title'], contents=request_post_params['contents'])
    writing.save()
    # 다:다 관계가 설정되어 있는 Tag 와 연결하기 위해 Writing 에 Tag 를 추가한다.
    for tag_query_set in tags_query_set:
        writing.tags.add(tag_query_set)
    # 메인 화면으로 리다이렉트
    return HttpResponseRedirect(reverse('writing:entrance'))
