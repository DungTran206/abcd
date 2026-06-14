from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Enrollment

# Tabular inline for displaying choices within questions
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

# Inline for questions within courses
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2

# Custom admin for Question model
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content', 'course', 'grade']

# Custom admin for Lesson model
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']

# Register all models
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Enrollment)
