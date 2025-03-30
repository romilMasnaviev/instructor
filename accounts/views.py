from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# POST /register - Регистрация нового пользователя
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        data = request.data

        # Валидация email
        email = data.get('email')
        if email:
            try:
                EmailValidator()(email)
            except ValidationError:
                return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

        # Валидация имени
        full_name = data.get('full_name')
        if not full_name or len(full_name.strip()) == 0:
            return Response({"error": "Full name is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка на существование email в базе данных
        if Account.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Создание аккаунта
        try:
            account = Account.objects.create(
                username=data['username'],
                email=email,
                password=data['password'],  # Пароль будет хэширован автоматически
                full_name=full_name,
            )
            account.save()

            # Сериализация пользователя и ответ
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except KeyError as e:
            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# GET /user/{user_id} - Получение информации о пользователе
@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = Account.objects.get(account_id=user_id)
    except Account.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AccountSerializer(user)
    return Response(serializer.data)


# PUT /user/{user_id}/update - Обновление данных пользователя
@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = Account.objects.get(account_id=user_id)
    except Account.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    if 'email' in data:
        # Валидация email
        email = data['email']
        try:
            EmailValidator()(email)
        except ValidationError:
            return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

    # Валидация полного имени
    full_name = data.get('full_name')
    if full_name and len(full_name.strip()) == 0:
        return Response({"error": "Full name cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

    # Обновляем данные пользователя
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'full_name' in data:
        user.full_name = full_name
    if 'password' in data:
        user.set_password(data['password'])

    user.save()

    serializer = AccountSerializer(user)
    return Response(serializer.data)


from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_id', 'username', 'email', 'created_at', 'full_name']
