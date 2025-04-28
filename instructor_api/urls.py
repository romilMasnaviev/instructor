from django.urls import path

from instructors import views
from instructors.views import instructor_schedule, training_group_detail

urlpatterns = [
    path('instructors/<int:instructor_id>/schedule/', instructor_schedule, name='instructor_schedule'),
    path('instructors/<int:instructor_id>/training_groups/<int:training_group_id>/', training_group_detail,
         name='training_group_detail'),

    path('instructors/<int:instructor_id>/training_groups/<int:training_group_id>/start/',
         views.start_training, name='start_training'),
    path('instructors/<int:instructor_id>/training_groups/<int:training_group_id>/complete/',
         views.complete_training, name='complete_training'),

    path(
        'instructors/<int:instructor_id>/training_groups/<int:training_group_id>/parachutists/<int:parachutist_id>/edit_checkpoint/',
        views.edit_checkpoint, name='edit_checkpoint'),
]
