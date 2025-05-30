from django.urls import path

from instructors import views
from instructors.views import instructor_schedule, training_group_detail, jump_group_detail

urlpatterns = [
    # Расписание
    path('instructors/<int:instructor_id>/schedule/',
         instructor_schedule,
         name='instructor_schedule'),

    # Учебные группы
    path('instructors/<int:instructor_id>/training_groups/<int:training_group_id>/',
         training_group_detail,
         name='training_group_detail'),
    path('instructors/<int:instructor_id>/training_groups/<int:training_group_id>/start/',
         views.start_training,
         name='start_training'),
    path('instructors/<int:instructor_id>/training_groups/<int:training_group_id>/complete/',
         views.complete_training,
         name='complete_training'),
    path(
        'instructors/<int:instructor_id>/training_groups/<int:training_group_id>/parachutists/<int:parachutist_id>/edit_checkpoint/',
        views.edit_training_checkpoint,
        name='edit_training_checkpoint'
    ),

    # Прыжковые группы
    path('instructors/<int:instructor_id>/jump_groups/<int:jump_group_id>/',
         jump_group_detail,
         name='jump_group_detail'),

    path('instructors/<int:instructor_id>/jump_groups/<int:jump_group_id>/start_pre_flight_preparation/',
         views.start_pre_flight_preparation,
         name='start_pre_flight_preparation'),

    path('instructors/<int:instructor_id>/jump_groups/<int:jump_group_id>/complete_pre_flight_preparation/',
         views.complete_pre_flight_preparation,
         name='complete_pre_flight_preparation'),

     path('instructors/<int:instructor_id>/jump_groups/<int:jump_group_id>/complete_jump_group/',
         views.complete_jump_group,
         name='complete_jump_group'),

    path(
        'instructors/<int:instructor_id>/jump_groups/<int:jump_group_id>/parachutists/<int:parachutist_id>/edit_jump_checkpoint/',
        views.edit_jump_checkpoint,
        name='edit_jump_checkpoint'
    ),

    path(
        'instructors/<int:instructor_id>/jump_groups/<int:jump_group_id>/parachutists/<int:parachutist_id>/set_jump_score/',
        views.set_jump_score,
        name='set_jump_score'),
    
    path('instructor/<int:instructor_id>/jump-group/<int:jump_group_id>/update-order/', 
         views.update_parachutist_order, 
         name='update_parachutist_order'),

]
