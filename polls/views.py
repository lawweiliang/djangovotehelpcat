from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Question, Choice

def index(request):
  question_list = Question.objects.order_by('pub_date')[:5]
  context = {
    'question_list': question_list
  }
  return render(request, 'polls/question.html', context)


def detail(request, question_id):
   question = get_object_or_404(Question, id=question_id)
   choice = question.choice_set.all();
   return render(request, 'polls/detail.html', {'question':question, 'choice':choice})


def vote(request, question_id):
  question = get_object_or_404(Question, id=question_id)
  try:
    selected_choice = question.choice_set.get(id=request.POST['choice'])
  except(KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.html', {
      'question': question,
      'error_message': 'You did\'t select a choice.'
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))


def result(request, question_id):
  question = get_object_or_404(Question, id=question_id)
  return render(request, 'polls/result.html', {'question':question})


def hello(request):
  return HttpResponse('yeah, you are now in hello page')