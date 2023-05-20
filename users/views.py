from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from users.exceptions import UniqueUserNameOrEmail
from users.permissions import IsUserPermission
from users.serializers import AccountSerializer, CustomJWTSerializer


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = AccountSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()

            return Response(serializer.data, status.HTTP_201_CREATED)
        except UniqueUserNameOrEmail as err:
            return Response(err.message, status.HTTP_400_BAD_REQUEST)


class loginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsUserPermission]

    def get(self, request: Request, id_user: int):
        user = get_object_or_404(User, id=id_user)

        self.check_object_permissions(request, user)

        serializer = AccountSerializer(instance=user)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, id_user: int):
        user = get_object_or_404(User, id=id_user)

        self.check_object_permissions(request, user)

        serializer = AccountSerializer(instance=user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)
