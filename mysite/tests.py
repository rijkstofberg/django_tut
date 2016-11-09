import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question


def create_question(question_text, hours):
    time = timezone.now() + datetime.timedelta(hours=hours)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    return question


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        future_question = create_question('Future question.', 30 * 24)
        self.assertIs(
            future_question.was_published_recently(),
            False,
            'The question is in the future!'
        )

    def test_was_published_recently_with_recent_question(self):
        recent_question = create_question('Recent question.', -1)
        self.assertIs(
            recent_question.was_published_recently(),
            True,
            'The question is recent!'
        )


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        resp = self.client.get(reverse('polls:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'No polls are available.')
        self.assertQuerysetEqual(resp.context['latest_question_list'], [])

    def test_index_view_with_question_in_past(self):
        question = create_question('Past question', -30 * 24)
        resp = self.client.get(reverse('polls:index'))
        fetched_questions = [q for q in resp.context['latest_question_list']]
        self.assertEqual(
            fetched_questions,
            [question, ],
            'We should have one current question.'
        )

    def test_index_view_with_2_questions_in_past(self):
        question1 = create_question('Past question', -10 * 24)
        question2 = create_question('Past question', -20 * 24)
        resp = self.client.get(reverse('polls:index'))
        fetched_questions = [q for q in resp.context['latest_question_list']]
        self.assertEqual(
            fetched_questions,
            [question1, question2],
            'We should have two current questions.'
        )

    def test_index_view_with_question_in_future(self):
        create_question('Future question', 30 * 24)
        resp = self.client.get(reverse('polls:index'))
        fetched_questions = [q for q in resp.context['latest_question_list']]
        self.assertEqual(
            fetched_questions,
            [],
            'There should be no current questions.'
        )

    def test_index_with_future_and_past_questions(self):
        future_question = create_question('Past question', 30 * 24)
        past_question = create_question('Past question', -30 * 24)
        resp = self.client.get(reverse('polls:index'))
        fetched_questions = [q for q in resp.context['latest_question_list']]
        self.assertEqual(
            fetched_questions,
            [past_question, ],
            'We should have one current question.'
        )


class QuestionDetailViewTests(TestCase):

    def test_detail_with_future_question(self):
        future_question = create_question('Future question', 30 * 24)
        resp = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(
            resp.status_code,
            404,
            'We should not be able to find question:%s' % future_question.id
        )

    def test_detail_with_past_question(self):
        past_question = create_question('Future question', -30 * 24)
        resp = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertEquals(
            resp.status_code,
            200,
            'We must be able to find question:%s' % past_question.id
        )
        self.assertEqual(
            resp.context['question'],
            past_question,
            'We should be able to find the question.'
        )
