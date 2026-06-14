from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # ... các đường dẫn khác (nếu có) ...
    
    # Nộp bài thi
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # Xem kết quả thi
    path('course/<int:course_id>/submission/<int:submission_id>/result/', 
         views.show_exam_result, name='exam_result'),
]
