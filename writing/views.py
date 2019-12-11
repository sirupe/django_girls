from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from writing.models import Writing, Tag, WritingsTag


def entrance(request):
    writings = Writing.objects.all().order_by('-uploaded_time')
    context = {'writings': writings}
    return render(request, 'writing/index.html', context)


def write_form(request):
    return render(request, 'writing/write_form.html')


def write(request):
    # 글을 저장한다.
    request_post_params = request.POST
    writing = Writing(title=request_post_params['title'], contents=request_post_params['contents'])
    writing.save()
    # 태그를 각각 분리한다(',')
    tags = request_post_params['tags'].split(',')
    # 분리한 태그들을 저장한다. 이 때 기존에 존재하는 태그는 insert 하지 않는다.
    #  -1. 입력된 태그와 중복되는 태그가 기존 테이블에 있는지 조회
    duplicated_tags = Tag.objects.filter(name__in=tags)
    duplicated_tag_names = set(map(lambda tag: tag.name, duplicated_tags))
    #  -2. -1 에서 조회된 데이터를 tags 에서 제외
    #  -3. tags 저장
    tags_set = []
    for tag in tags:
        if not tag in duplicated_tag_names:
            tags_set.append(Tag(name=tag))
    inserted_tags = Tag.objects.bulk_create(tags_set)
    # 저장된 글과 사용자가 입력한 태그들의 id 를 writingstag 테이블에 저장한다. 이 때 중복값은 절대 발생하지 않는다.
    for tag in (inserted_tags.extend(duplicated_tags)):
        WritingsTag(tag_id=tag, writing_id=writing).save()
    # 메인 화면으로 리다이렉트
    return HttpResponseRedirect(reverse('writing:entrance'))
