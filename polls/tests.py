import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice

# Create your tests here.

def create_question(question_text, days):
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text, pub_date = time)


class indexFunctionTest(TestCase):
  def test_index_page_no_question(self):
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Database have no question.')
    self.assertQuerysetEqual(response.context['question_list'], [])

  def test_index_page_with_question(self):
    question = create_question(question_text='What your favourite food?', days=3)
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['question_list'], [question])

  def test_index_page_with_two_question(self):
    question1 = create_question(question_text='What your name?', days=2)
    question2 = create_question(question_text='What your favourite books?', days=2)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context['question_list'], [question1, question2])


class detailFunctionTest(TestCase):
  def test_detail_page_no_id(self):
    response = self.client.get(reverse('polls:questionDetail', args=(0,)))
    self.assertEqual(response.status_code, 404)

  def test_detail_page_with_question_and_choice(self):
    question = create_question(question_text='What your favourite food?', days=3)
    choice = question.choice_set.create(choice_text="nasi lemak", votes=0)
    response = self.client.get(reverse('polls:questionDetail', args=(1,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'What your favourite food?')
    self.assertEqual(response.context['question'], question)
    self.assertQuerysetEqual(response.context['choice'], [choice])

  def test_detail_page_with_question_and_multiple_choice(self):
    question = create_question(question_text='What your favourite food?', days=3)
    choice1 = question.choice_set.create(choice_text='nasi lemak', votes=0)
    choice2 = question.choice_set.create(choice_text='coca cola', votes=0)
    response = self.client.get(reverse('polls:questionDetail', args=(1,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'What your favourite food?')
    self.assertEqual(response.context['question'], question)
    self.assertQuerysetEqual(response.context['choice'], [choice1, choice2], ordered=False)

  def test_detail_page_with_no_choice(self):
    question = create_question(question_text='What your favourite food?', days=3)
    response =  self.client.get(reverse('polls:questionDetail', args=(1,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Question does not have choice.')

  
class voteFunctionTest(TestCase):
  def test_vote_page_with_no_id(self):
    response = self.client.get(reverse('polls:vote', args=(0,)))
    self.assertEqual(response.status_code, 404)

  def test_vote_page_select_choice(self):
    question = create_question(question_text='What your favourite food?', days=3)
    choice = question.choice_set.create(choice_text='nasi lemak', votes=0)
    response = self.client.post(reverse('polls:vote', args=(1,)), {'choice': choice.id})

    choiceUpdate = question.choice_set.get(id=choice.id)
    self.assertEqual(response.status_code, 302)
    self.assertEqual(choiceUpdate.votes, 1)


class resultFunctionTest(TestCase):
  def test_result_page_with_no_id(self):
    response = self.client.get(reverse('polls:vote', args=(0,)))
    self.assertEqual(response.status_code, 404)

  def test_result_page_with_no_id(self):
    question = create_question(question_text='What your favourite food?', days=3)
    choice = question.choice_set.create(choice_text='nasi lemak', votes=0)
    response = self.client.get(reverse('polls:result', args=(1,)));
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'What your favourite food?')
    self.assertContains(response, 'nasi lemak')
    self.assertContains(response, '0')
    
