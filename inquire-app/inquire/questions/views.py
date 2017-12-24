from django.shortcuts import render, get_object_or_404
from inquire.questions.models import Question, Answer, Tag
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone, feedgenerator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging


logger = logging.getLogger(__name__)


def tag_handler(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    question_list = sorted(tag.question_set.all(), key=lambda x: x.pub_date,
                           reverse=True)
    paginator = Paginator(question_list, 10)
    page = request.GET.get('page')

    try:
        latest_question_list = paginator.page(page)
    except PageNotAnInteger:
        latest_question_list = paginator.page(1)
    except EmptyPage:
        latest_question_list = paginator.page(paginator.num_pages)

    context = {
        'latest_question_list': latest_question_list,
        'username': request.user.first_name,
        'tag': tag.tag
    }
    return render(request, 'questions/index.html', context)


def index(request):
    print('>>>>>>>>>>>>>>>>', request.user)
    question_list = Question.objects.order_by('-pub_date')
    paginator = Paginator(question_list, 10)
    page = request.GET.get('page')

    try:
        latest_question_list = paginator.page(page)
    except PageNotAnInteger:
        latest_question_list = paginator.page(1)
    except EmptyPage:
        latest_question_list = paginator.page(paginator.num_pages)

    context = {'latest_question_list': latest_question_list}

    return render(request, 'questions/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.filter(question_id=question_id)

    return render(request, 'questions/detail.html', {
        'question': question,
        'answers': answers,
        'username': request.user.first_name,
        'taglist': question.tags.all
    }, )


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.filter(question_id=question_id)
    return render(request, 'questions/results.html', {'question': question, 'answers': answers})


def question_vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)

    if 'VoteUpQuestion' in request.POST:
        if request.user not in p.up_list.all():
            p.up_list.add(request.user)
            p.up_votes += 1

    elif 'VoteDownQuestion' in request.POST:
        if request.user not in p.down_list.all():
            p.down_list.add(request.user)
            p.down_votes += 1

    p.save()


@login_required
def vote(request, question_id):
    if 'VoteUpQuestion' in request.POST or 'VoteDownQuestion' in request.POST:
        question_vote(request, question_id)
        return HttpResponseRedirect(reverse('questions:detail', args=(question_id,)))

    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = Answer.objects.get(pk=request.POST['answer'])
    except (KeyError, Answer.DoesNotExist):
        return render(request, 'questions/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        if 'VoteUp' in request.POST:
            if request.user not in selected_choice.up_list.all():
                selected_choice.up_list.add(request.user)
                selected_choice.up_votes += 1

            selected_choice.net_votes = selected_choice.up_votes-selected_choice.down_votes
        elif 'VoteDown' in request.POST:
            if request.user not in selected_choice.down_list.all():
                selected_choice.down_list.add(request.user)
                selected_choice.down_votes += 1

            selected_choice.net_votes = selected_choice.up_votes-selected_choice.down_votes

        selected_choice.save()
        return HttpResponseRedirect(reverse('questions:detail', args=(p.id,)))


@login_required
def goto_add_page(request):
    context = {'username': request.user.first_name}
    return render(request, 'questions/ask.html', context)


def add_question(request):
    if 'Submit' in request.POST:
        new_question_title = request.POST['question_title']
        new_question_text = request.POST['question_text']
        new_question = Question(question_text=new_question_text, pub_date=timezone.now(), author=request.user,
                                modification_time=timezone.now(), question_title=new_question_title)
        tag_string = request.POST['tags']
        tags = tag_string.split(',')

        new_question.save()
        for new_tag in tags:
            new_tag_object = Tag(tag=new_tag)

            if Tag.objects.filter(tag=new_tag):
                new_question.tags.add(Tag.objects.get(tag=new_tag))
            else:
                new_tag_object.save()
                new_question.tags.add(new_tag_object)

        new_question.save()
        return HttpResponseRedirect(reverse('questions:index'))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('questions:ask'))
    else:
        return HttpResponse("Submit new question error")


@login_required
def goto_answer_page(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    context = {'question': p, 'username': request.user.first_name}
    return render(request, 'questions/answer.html', context)


def add_answer(request, question_id):
    if 'Submit' in request.POST:
        p = get_object_or_404(Question, pk=question_id)
        new_answer_text = request.POST['answer_text']
        new_answer = Answer(answer_text=new_answer_text, pub_date=timezone.now(), author=request.user, question=p,
                             modification_time=timezone.now())
        new_answer.save()
        p.number_of_answers = len(Answer.objects.filter(question_id=question_id).all())
        p.save()
        return HttpResponseRedirect(reverse('questions:detail', args=(question_id,)))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('questions:detail', args=(question_id,)))
    else:
        return HttpResponse("Submit new answer error")


@login_required
def edit_question_page(request, question_id):
    p = get_object_or_404(Question, pk=question_id)

    can_edit = False
    if request.user == p.author:
        can_edit = True

    context = {'question': p, "can_edit": can_edit}
    return render(request, 'questions/edit_question_page.html', context)


def edit_question(request, question_id):
    if 'Submit' in request.POST:
        p = get_object_or_404(Question, pk=question_id)
        p.question_text = request.POST['question_text']
        p.question_title = request.POST['question_title']
        p.modification_time = timezone.now()
        p.save()
        return HttpResponseRedirect(reverse('questions:detail', args=(question_id,)))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('questions:detail', args=(question_id,)))
    else:
        return HttpResponse("Submit new answer error")


@login_required
def edit_answer_page(request, question_id, answer_id):
    p = get_object_or_404(Answer, pk=answer_id)
    q = get_object_or_404(Question, pk=question_id)

    can_edit = False
    if request.user == p.author:
        can_edit = True

    context = {'answer': p, "can_edit": can_edit, 'question': q}
    return render(request, 'questions/edit_answer_page.html', context)


def edit_answer(request, question_id, answer_id):
    if 'Submit' in request.POST:
        p = get_object_or_404(Answer, pk=answer_id)
        p.answer_text = request.POST['answer_text']
        p.modification_time = timezone.now()
        p.save()
        return HttpResponseRedirect(reverse('questions:detail', args=(question_id,)))
    elif 'Cancel' in request.POST:
        return HttpResponseRedirect(reverse('questions:detail', args=(question_id,)))
    else:
        return HttpResponse("Submit new answer error")


def rss(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.filter(question_id=question_id)

    feed = feedgenerator.Rss201rev2Feed(
        title="Output question rss",
        link="",
        description=u"This is the content of all staff related to one question.",
        language=u"en",
    )

    feed.add_item(
        title=question.question_title,
        link=u"",
        description=question.question_text)

    for answer in answers:
        feed.add_item(
            title=u"answer",
            link="",
            description=answer.answer_text,)

    str=feed.writeString('utf-8')

    context = {}
    str = format(str)
    context['str'] = str

    return render(request, 'questions/rss.html', context)


def format(str):
    str = str.replace('>', '>\n')
    str = str.replace('<', '\n<')
    str = str.replace('\n\n', '\n')

    return str
