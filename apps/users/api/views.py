from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user": {"email": user.email, "id": user.id},
                "message": "User created successfully.",
            },
            status=status.HTTP_201_CREATED,
        )
