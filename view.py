from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission

def submit(request, course_id):
    """Handle exam submission"""
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    # Create submission and save selected choices
    submission = Submission.objects.create(enrollment=enrollment)
    choices = extract_answers(request)
    submission.choices.set(choices)
    
    return HttpResponseRedirect(reverse('onlinecourse:exam_result', 
                                        args=(course_id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    """Calculate and display exam results"""
    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.get(id=submission_id)
    choices = submission.choices.all()
    
    # Calculate total score
    total_score = 0
    for choice in choices:
        if choice.is_correct:
            total_score += choice.question.grade
    
    context = {
        'course': course,
        'grade': total_score,
        'choices': choices
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

def extract_answers(request):
    """Extract selected choice IDs from POST request"""
    selected = []
    for key in request.POST:
        if key.startswith('choice_'):
            value = request.POST[key]
            choice_id = int(value)
            selected.append(choice_id)
    return selected
