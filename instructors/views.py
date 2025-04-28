# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import TrainingGroup, JumpGroup, Instructor, TrainingGroupParachutist
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import TrainingGroupParachutist, TrainingGroup, Instructor

# Инструктор получает расписание
def instructor_schedule(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)

    # Учебные группы
    training_groups = TrainingGroup.objects.filter(instructor=instructor)

    # Прыжковые группы
    jump_groups = JumpGroup.objects.filter(
        Q(instructor_air=instructor) | Q(instructor_ground=instructor)
    )

    context = {
        'instructor': instructor,
        'training_groups': training_groups,
        'jump_groups': jump_groups,
    }

    return render(request, 'instructor_schedule.html', context)

# Инструктор получает учебную группу
def training_group_detail(request, instructor_id, training_group_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    training_group = get_object_or_404(TrainingGroup, pk=training_group_id, instructor=instructor)

    # Подгружаем парашютистов этой группы
    group_parachutists = TrainingGroupParachutist.objects.filter(group=training_group).select_related('parachutist')

    context = {
        'instructor': instructor,
        'training_group': training_group,
        'group_parachutists': group_parachutists,
    }

    return render(request, 'training_group_detail.html', context)

# Инструктор начинает обучение учебной группы
def start_training(request, instructor_id, training_group_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    training_group = get_object_or_404(TrainingGroup, pk=training_group_id, instructor=instructor)

    if training_group.status != 'created':
        return HttpResponseForbidden("Группу нельзя начать, она уже в процессе или завершена.")

    training_group.status = 'in_progress'
    training_group.save()

    return redirect('training_group_detail', instructor_id=instructor_id, training_group_id=training_group_id)

# Инструктор заканчивает обучение учебной группы
def complete_training(request, instructor_id, training_group_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    training_group = get_object_or_404(TrainingGroup, pk=training_group_id, instructor=instructor)

    if training_group.status != 'in_progress':
        return HttpResponseForbidden("Группу нельзя завершить, она не в процессе обучения.")

    training_group.status = 'completed'
    training_group.save()

    return redirect('training_group_detail', instructor_id=instructor_id, training_group_id=training_group_id)

# Инструктор изменяет чекпоинты парашютиста в учебной группе
def edit_checkpoint(request, instructor_id, training_group_id, parachutist_id):
    parachutist_group = get_object_or_404(TrainingGroupParachutist, parachutist_id=parachutist_id,
                                          group_id=training_group_id)
    training_group = get_object_or_404(TrainingGroup, group_id=training_group_id)

    # Получаем инструктора по его ID
    instructor = get_object_or_404(Instructor, instructor_id=instructor_id)

    if request.method == 'POST':
        # Обновляем значения чекпоинтов
        parachutist_group.theory_passed = 'theory_passed' in request.POST
        parachutist_group.practice_passed = 'practice_passed' in request.POST
        parachutist_group.exam_passed = 'exam_passed' in request.POST

        # Сохраняем изменения
        parachutist_group.save()

        # Перенаправляем обратно на страницу редактирования
        return redirect('edit_checkpoint', instructor_id=instructor_id, training_group_id=training_group_id,
                        parachutist_id=parachutist_id)

    return render(request, 'edit_checkpoint.html', {
        'parachutist_group': parachutist_group,
        'training_group': training_group,
        'instructor': instructor,
    })
