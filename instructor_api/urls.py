from instructors import views
from instructors.views import instructor_schedule, complete_training

urlpatterns = [

]
from django.urls import path

urlpatterns = [
    # Просмотр расписания
    path('instructor/<int:instructor_id>/schedule/', instructor_schedule, name='instructor_schedule'),
    # Просмотр конкретной прыжковой группы
    path('instructor/<int:instructor_id>/training-groups/<int:group_id>/', views.training_group_detail_view,
         name='training_group_detail'),
    # Начало обучения конкретной группы
    path('training-group/start/<int:group_id>/', views.start_training, name='start_training'),
    # Завершение обучения конкретной группы
    path('training-group/complete/<int:group_id>/', views.complete_training, name='complete_training'),


    path('update_theory/<int:parachutist_id>/<int:group_id>/', views.update_theory, name='update_theory'),
    path('update_practice/<int:parachutist_id>/<int:group_id>/', views.update_practice, name='update_practice'),
    path('update_exam/<int:parachutist_id>/<int:group_id>/', views.update_exam, name='update_exam'),

]
