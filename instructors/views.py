from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import Account
from .models import Instructor
from .serializers import InstructorSerializer


# POST /instructors - Регистрация нового инструктора
@api_view(['POST'])
def create_instructor(request):
    if request.method == 'POST':
        data = request.data
        try:
            # Получаем Account по email
            account = Account.objects.get(email=data['email'])

            # Проверка наличия и непустого значения qualification
            qualification = data.get('qualification')
            if not qualification or len(qualification.strip()) == 0:
                return Response({"error": "Qualification is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Создаем инструктора
            instructor = Instructor.objects.create(
                account=account,
                qualification=qualification,
                status="Active"
            )
            instructor.name = data.get("name", "")
            instructor.save()

            # Сериализация и ответ
            serializer = InstructorSerializer(instructor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Account.DoesNotExist:
            return Response({"error": "Account with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# PUT /instructors/{instructor_id} - Обновление данных инструктора
@api_view(['PUT'])
def update_instructor(request, instructor_id):
    try:
        instructor = Instructor.objects.get(instructor_id=instructor_id)
    except Instructor.DoesNotExist:
        return Response({"error": "Instructor not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        data = request.data
        instructor.qualification = data.get('qualification', instructor.qualification)
        instructor.status = data.get('status', instructor.status)
        instructor.save()
        serializer = InstructorSerializer(instructor)
        return Response(serializer.data)

# PATCH /instructors/{instructor_id}/qualification - Обновление квалификации инструктора
@api_view(['PATCH'])
def update_instructor_qualification(request, instructor_id):
    try:
        instructor = Instructor.objects.get(instructor_id=instructor_id)
    except Instructor.DoesNotExist:
        return Response({"error": "Instructor not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        data = request.data
        instructor.qualification = data.get('qualification', instructor.qualification)
        instructor.save()
        serializer = InstructorSerializer(instructor)
        return Response(serializer.data)
