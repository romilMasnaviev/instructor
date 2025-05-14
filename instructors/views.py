# views.py
import json
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Instructor, JumpGroupParachutist, Parachutist
from .models import TrainingGroupParachutist, TrainingGroup


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
def edit_training_checkpoint(request, instructor_id, training_group_id, parachutist_id):
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
        parachutist_group.medical_certified = 'medical_certified' in request.POST

        # Сохраняем изменения
        parachutist_group.save()

        # Перенаправляем обратно на страницу редактирования
        return redirect('edit_training_checkpoint', instructor_id=instructor_id, training_group_id=training_group_id,
                        parachutist_id=parachutist_id)

    return render(request, 'edit_training_checkpoint.html', {
        'parachutist_group': parachutist_group,
        'training_group': training_group,
        'instructor': instructor,
    })


# Инструктор получает прыжковую группу
def jump_group_detail(request, instructor_id, jump_group_id):
    instructor = get_object_or_404(Instructor, instructor_id=instructor_id)
    jump_group = get_object_or_404(JumpGroup, id=jump_group_id)

    sort_by = request.GET.get('sort_by', 'default')

    return render(request, 'jump_group_detail.html', {
        'instructor': instructor,
        'jump_group': jump_group,
        'request_data': get_parachutists_for_jump_group_detail(jump_group=jump_group, sort_by=sort_by),
        'sort_by': sort_by,
    })

@csrf_exempt
def update_parachutist_order(request, instructor_id, jump_group_id):
    if request.method == 'POST':
        try:
            # Получение данных из JSON-тела запроса
            data = json.loads(request.body)
            order_data = data.get('order', [])

            for index, parachutist_id in enumerate(order_data, start=1):
                JumpGroupParachutist.objects.filter(
                    jump_group_id=jump_group_id,
                    parachutist_id=parachutist_id
                ).update(custom_order=index)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error'}, status=405)


# Инструктор начинает предполетную подготовку
def start_pre_flight_preparation(request, instructor_id, jump_group_id):
    jump_group = get_object_or_404(JumpGroup, id=jump_group_id)

    # Изменение статуса группы
    jump_group.status = 'Pre-Flight Preparation'
    jump_group.save()

    # Получаем всех парашютистов в этой группе
    jump_group_parachutists = JumpGroupParachutist.objects.filter(jump_group=jump_group)

    # Обнуляем чекпоинты для каждого парашютиста
    for jgp in jump_group_parachutists:
        jgp.medical_checkup_passed = False
        jgp.equipment_checked = False
        jgp.correct_assignment = False
        jgp.save()

    return redirect('jump_group_detail', instructor_id=instructor_id, jump_group_id=jump_group_id)


def edit_jump_checkpoint(request, instructor_id, jump_group_id, parachutist_id):
    # Находим заявку парашютиста на прыжок в конкретной группе
    parachutist_group = get_object_or_404(JumpGroupParachutist, parachutist_id=parachutist_id,
                                          jump_group_id=jump_group_id)
    # Находим прыжковую группу
    jump_group = get_object_or_404(JumpGroup, id=jump_group_id)
    parachutist = get_object_or_404(Parachutist, parachutist_id=parachutist_id)
    jump_assignment = JumpAssignment.objects.filter(jump_group=jump_group, parachutist=parachutist)

    # Находим парашютиста в учебной группе
    parachutist_in_training_group = TrainingGroupParachutist.objects.filter(parachutist=parachutist).first()

    # Находим инструктора
    instructor = get_object_or_404(Instructor, instructor_id=instructor_id)

    if request.method == 'POST':
        # Обновляем чекпоинты из формы
        parachutist_group.theory_passed = 'theory_passed' in request.POST
        parachutist_group.practice_passed = 'practice_passed' in request.POST
        parachutist_group.medical_checkup_passed = 'medical_checkup_passed' in request.POST
        parachutist_group.equipment_checked = 'equipment_checked' in request.POST
        parachutist_group.correct_assignment = 'correct_assignment' in request.POST

        # Сохраняем изменения
        parachutist_group.save()

        # После сохранения перенаправляем обратно
        return redirect('edit_jump_checkpoint', instructor_id=instructor_id, jump_group_id=jump_group_id,
                        parachutist_id=parachutist_id)

    return render(request, 'edit_jump_checkpoint.html', {
        'parachutist_in_training_group': parachutist_in_training_group,
        'parachutist_group': parachutist_group,
        'jump_group': jump_group,
        'instructor': instructor,
        'jump_assignment': jump_assignment,
    })


# Инструктор заканчивает предполетную подготовку, статус у прыжкового парашютиста
# выставляется на Approved или Denied
def complete_pre_flight_preparation(request, instructor_id, jump_group_id):
    jump_group = get_object_or_404(JumpGroup, id=jump_group_id)

    # Получаем все заявки на прыжок в группе
    jump_group_parachutists = JumpGroupParachutist.objects.filter(jump_group_id=jump_group_id)

    # Обновляем статус заявок на основе выполнения чекпоинтов
    for parachutist_group in jump_group_parachutists:
        parachutist_training = TrainingGroupParachutist.objects.filter(
            parachutist_id=parachutist_group.parachutist.parachutist_id).first()
        if (parachutist_training.theory_passed and parachutist_training.practice_passed and
                #  parachutist_training.medical_certified and
                parachutist_group.medical_checkup_passed and
                parachutist_group.equipment_checked and parachutist_group.correct_assignment):
            parachutist_group.request_status = 'Approved'  # Если все чекпоинты выполнены
        else:
            parachutist_group.request_status = 'Denied'  # Если хотя бы один чекпоинт не выполнен
        parachutist_group.save()

    # Изменяем статус группы на 'Jump In Progress'
    jump_group.status = 'Jump In Progress'
    jump_group.save()

    # Перенаправляем на детальную страницу прыжковой группы
    return redirect('jump_group_detail', instructor_id=instructor_id, jump_group_id=jump_group_id)


from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import JumpGroup, JumpAssignment


def set_jump_score(request, instructor_id, jump_group_id, parachutist_id):
    # Получаем объект прыжковой группы
    jump_group = get_object_or_404(JumpGroup, id=jump_group_id)

    instructor = get_object_or_404(Instructor, instructor_id=instructor_id)

    # Проверяем, что группа находится в статусе 'Jump In Progress'
    if jump_group.status != 'Jump In Progress':
        return HttpResponseForbidden("Группа не в процессе прыжка")

    # Получаем объект парашютиста и задание для него
    parachutist = get_object_or_404(Parachutist, parachutist_id=parachutist_id)
    jump_assignment = get_object_or_404(JumpAssignment, jump_group=jump_group, parachutist=parachutist)

    if request.method == "POST":
        # Получаем оценку из формы
        score = request.POST.get("score")
        if score is not None:
            score = int(score)
            if 0 <= score <= 5:
                jump_assignment.score = score
                jump_assignment.completed = True  # Устанавливаем статус как выполнено
                jump_assignment.save()
                return redirect('jump_group_detail', instructor_id=instructor_id, jump_group_id=jump_group_id)
        return HttpResponseForbidden("Неверная оценка")

    return render(request, 'set_jump_score.html', {
        'jump_group': jump_group,
        'parachutist': parachutist,
        'jump_assignment': jump_assignment,
        'instructor': instructor  # Передаем объект инструктора в контекст
    })


def complete_jump_group(request, instructor_id, jump_group_id):
    jump_group = get_object_or_404(JumpGroup, id=jump_group_id)
    instructor = get_object_or_404(Instructor, instructor_id=instructor_id)
    error_message = None
    allowed_group_status = jump_group.status == 'Jump In Progress'

    if not allowed_group_status:
        error_message = 'Неподходящий статус прыжковой группы: завершение доступно только после стадии `Прыжок в процессе`'
    else:
        parachutists_ids = JumpGroupParachutist.objects.filter(
            jump_group_id=jump_group_id,
            request_status='Approved'
        ).values_list('parachutist_id', flat=True)

        if not all_parachutists_complete_jump(parachutists_ids=parachutists_ids, jump_group_id=jump_group_id):
            error_message = '''Не все допущенные до прыжка парашютисты завершили прыжок или не всем выставлена оценка за него. 
            Прыжковая группа не может быть завершена.'''
        else:
            jump_group.status = 'Completed'
            jump_group.save()
            return redirect('jump_group_detail', instructor_id=instructor_id, jump_group_id=jump_group_id)

    return render(request, 'jump_group_detail.html', {
        'jump_group': jump_group,
        'instructor': instructor,
        'request_data': get_parachutists_for_jump_group_detail(jump_group=jump_group),
        'error_message': error_message
    })


def all_parachutists_complete_jump(parachutists_ids, jump_group_id):
    for parachutist_id in parachutists_ids:
        result = JumpAssignment.objects.get(jump_group_id=jump_group_id, parachutist_id=parachutist_id)
        if result.completed != True or result.score is None:
            return False
    return True


def get_parachutists_for_jump_group_detail(jump_group, sort_by=None):
    if jump_group.status == 'Jump In Progress':
        jump_group_parachutists = JumpGroupParachutist.objects.filter(jump_group=jump_group, request_status='Approved')
    else:
        # В противном случае показываем всех парашютистов группы
        jump_group_parachutists = JumpGroupParachutist.objects.filter(jump_group=jump_group)

    if sort_by == 'custom':
        jump_group_parachutists = jump_group_parachutists.order_by('custom_order')
    elif sort_by is None:
        ...
    elif sort_by == 'default' or sort_by is None:
        jump_group_parachutists = jump_group_parachutists.order_by(
            '-parachutist__weight',
            'jump_group__altitude'
        )

    # Для каждого парашютиста найдем задание (если есть)
    request_data = []
    for jgp in jump_group_parachutists:
        assignment = JumpAssignment.objects.filter(parachutist=jgp.parachutist, jump_group=jump_group).first()
        task = assignment.task if assignment else None
        score = assignment.score if assignment else None

        request_data.append({
            'request': jgp,  # Сам объект JumpGroupParachutist
            'task': task,
            'score': score
        })
        

    return request_data
