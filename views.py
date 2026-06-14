from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission

def extract_answers(request):
    selected = []
    for key in request.POST:
        if key.startswith('choice_'):
            choice_id = int(request.POST[key])
            selected.append(choice_id)
    return selected

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    submission = Submission.objects.create(enrollment=enrollment)
    selected_choices = extract_answers(request)
    submission.choices.set(selected_choices)
    
    return HttpResponseRedirect(reverse('onlinecourse:exam_result', args=(course_id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.get(id=submission_id)
    selected_choices = submission.choices.all()
    
    questions = Question.objects.filter(course=course)
    total_grade = 0
    possible_score = 0
    
    for question in questions:
        selected_ids = [choice.id for choice in selected_choices if choice.question == question]
        if question.is_get_score(selected_ids):
            total_grade += question.grade
        possible_score += question.grade
    
    context = {
        'course': course,
        'grade': total_grade,
        'possible': possible_score,
        'choices': selected_choices,
        'questions': questions,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
