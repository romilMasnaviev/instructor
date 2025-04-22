# views.py

from django.db import models
from django.http import Http404
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render

from .models import JumpGroup, Instructor, JumpRequest, PreJumpCheck
from .models import TrainingGroup
from .models import TrainingGroupParachutist, JumpAssignment


# Получение расписания инструктора
def instructor_schedule(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)

    # Учебные группы
    training_groups = TrainingGroup.objects.filter(instructor=instructor)

    # Прыжковые группы (где инструктор - либо воздушный, либо наземный)
    jump_groups = JumpGroup.objects.filter(
        models.Q(instructor_air=instructor) | models.Q(instructor_ground=instructor)
    )

    # Добавим поле group_type в каждый объект, чтобы различать типы в шаблоне
    for g in training_groups:
        g.group_type = 'учебная'
    for g in jump_groups:
        g.group_type = 'прыжковая'

    # Объединяем группы
    all_groups = sorted(list(training_groups) + list(jump_groups),
                        key=lambda x: x.start_date_time if hasattr(x, 'start_date_time') else x.jump_date)

    return render(request, 'schedule.html', {
        'instructor': instructor,
        'groups': all_groups,
    })


# Получение конкретной учебной группы
def training_group_detail_view(request, instructor_id, group_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    group = get_object_or_404(TrainingGroup, pk=group_id, instructor=instructor)
    trainees = TrainingGroupParachutist.objects.filter(group=group).select_related('parachutist')

    if request.method == 'POST':
        # Обрабатываем форму для каждого парашютиста
        for trainee in trainees:
            trainee.theory_passed = request.POST.get(f'theory_passed_{trainee.pk}') == 'on'
            trainee.practice_passed = request.POST.get(f'practice_passed_{trainee.pk}') == 'on'
            trainee.exam_passed = request.POST.get(f'exam_passed_{trainee.pk}') == 'on'
            trainee.ready_for_jump = request.POST.get(f'ready_for_jump_{trainee.pk}') == 'on'
            trainee.save()  # Сохраняем изменения

        return redirect('training_group_detail', instructor_id=instructor_id, group_id=group_id)

    context = {
        'instructor': instructor,
        'group': group,
        'trainees': trainees,
    }

    return render(request, 'training_group_detail.html', context)


# Обработчик для изменения статуса группы на "in_progress"
def start_training(request, group_id):
    # Получаем учебную группу по group_id
    group = get_object_or_404(TrainingGroup, pk=group_id)

    # Проверяем, что группа ещё не в процессе обучения
    if group.status != 'in_progress':
        group.status = 'in_progress'  # Изменяем статус
        group.save()  # Сохраняем изменения в базе данных

    # Получаем инструктора для перенаправления
    instructor_id = group.instructor.pk

    # После изменения статуса перенаправляем пользователя обратно на страницу группы
    return redirect('training_group_detail', instructor_id=instructor_id, group_id=group_id)


# Обработчик для изменения статуса группы на "completed"
def complete_training(request, group_id):
    # Получаем учебную группу по group_id
    group = get_object_or_404(TrainingGroup, pk=group_id)

    # Проверяем, что группа сейчас в процессе обучения
    if group.status == 'in_progress':
        group.status = 'completed'  # Изменяем статус
        group.save()  # Сохраняем изменения в базе данных

    # Получаем инструктора для перенаправления
    instructor_id = group.instructor.pk

    # Перенаправляем обратно на страницу группы
    return redirect('training_group_detail', instructor_id=instructor_id, group_id=group_id)


def update_theory(request, parachutist_id, group_id):
    if request.method == 'POST':
        record = get_object_or_404(
            TrainingGroupParachutist,
            parachutist__parachutist_id=parachutist_id,
            group__group_id=group_id
        )
        record.theory_passed = not record.theory_passed
        _recalculate_ready_for_jump(record)
    return redirect('training_group_detail', instructor_id=record.group.instructor.instructor_id, group_id=group_id)


def update_practice(request, parachutist_id, group_id):
    if request.method == 'POST':
        record = get_object_or_404(
            TrainingGroupParachutist,
            parachutist__parachutist_id=parachutist_id,
            group__group_id=group_id
        )
        record.practice_passed = not record.practice_passed
        _recalculate_ready_for_jump(record)
    return redirect('training_group_detail', instructor_id=record.group.instructor.instructor_id, group_id=group_id)


def update_exam(request, parachutist_id, group_id):
    if request.method == 'POST':
        record = get_object_or_404(
            TrainingGroupParachutist,
            parachutist__parachutist_id=parachutist_id,
            group__group_id=group_id
        )
        record.exam_passed = not record.exam_passed
        _recalculate_ready_for_jump(record)
    return redirect('training_group_detail', instructor_id=record.group.instructor.instructor_id, group_id=group_id)


def _recalculate_ready_for_jump(record):
    record.ready_for_jump = (
            record.theory_passed and
            record.practice_passed and
            record.exam_passed
    )
    record.save()


def jump_group_detail(request, instructor_id, group_id):
    # Получаем объект инструктора по его ID
    instructor = get_object_or_404(Instructor, pk=instructor_id)

    # Получаем прыжковую группу по group_id
    group = get_object_or_404(JumpGroup, pk=group_id)

    # Проверяем, что группа принадлежит данному инструктору (если необходимо)
    if group.instructor_ground != instructor and group.instructor_air != instructor:
        raise Http404("Доступ запрещен: Инструктор не связан с данной группой")

    # Получаем заявки на прыжок для этой группы
    jump_requests = JumpRequest.objects.filter(jump_group=group)

    # Получаем задания для парашютистов в этой группе
    jump_assignments = JumpAssignment.objects.filter(jump_group=group)

    # Получаем проверки перед прыжком для парашютистов в этой группе
    pre_jump_checks = PreJumpCheck.objects.filter(jump_group=group)

    context = {
        'group': group,
        'instructor': instructor,
        'jump_requests': jump_requests,
        'jump_assignments': jump_assignments,
        'pre_checks': pre_jump_checks,  # вот здесь ключ меняем
        'instructor_id': instructor.instructor_id,
    }

    return render(request, 'jump_group_detail.html', context)


def start_jump_group(request, instructor_id, group_id):
    # Получаем прыжковую группу
    group = get_object_or_404(JumpGroup, pk=group_id)

    # Получаем инструктора
    instructor = get_object_or_404(Instructor, pk=instructor_id)

    # Проверка, что инструктор может менять статус группы
    if instructor not in [group.instructor_air, group.instructor_ground]:
        return HttpResponseForbidden("Инструктор не назначен на эту группу.")

    # Проверка, что группа в статусе 'Created'
    if group.status != 'Created':
        return HttpResponseForbidden("Группа не может быть переведена в 'В процессе'.")

    # Изменяем статус группы на 'Progress'
    group.status = 'Progress'
    group.save()

    # Получаем все заявки на прыжок для данной группы
    jump_requests = JumpRequest.objects.filter(jump_group=group)

    # Создаем объект PreJumpCheck для каждого парашютиста
    for jump_request in jump_requests:
        parachutist = jump_request.parachutist

        training_group_parachutist = TrainingGroupParachutist.objects.filter(parachutist=parachutist).first()

        # Если такая запись существует, подгружаем нужные значения
        if training_group_parachutist:
            theory_passed = training_group_parachutist.theory_passed
            practice_passed = training_group_parachutist.practice_passed
        else:
            # Если записи нет, устанавливаем значения по умолчанию
            theory_passed = False
            practice_passed = False

        # Проверяем, есть ли уже проверка перед прыжком для этого парашютиста
        pre_jump_check = PreJumpCheck.objects.filter(jump_group=group, parachutist=parachutist).first()

        # Если проверка еще не существует, создаем новую запись
        if not pre_jump_check:
            # Создаем запись PreJumpCheck с подгруженными значениями
            PreJumpCheck.objects.create(
                jump_group=group,
                parachutist=parachutist,
                theory_passed=theory_passed,
                practice_passed=practice_passed,
                medical_certified=False,
                equipment_checked=False  # По умолчанию оставляем False
            )

    # Перенаправляем обратно на страницу группы
    return redirect('jump_group_detail', instructor_id=instructor_id, group_id=group.id)