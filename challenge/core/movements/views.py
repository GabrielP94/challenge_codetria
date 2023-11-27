from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Movement
from core.movements.serializers import MovementSerializer


class MovementCreate(APIView):
    """
    This view lists all clients and allows you to create a new one.
    """
    serializer_class = MovementSerializer

    def post(self, request):
        serializer = MovementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovementDetailDelete(APIView):
    """
    This view returns specific client information and allows you to delete it and update it.
    """
    def get_object(self, pk):
        try:
            return Movement.objects.get(pk=pk)
        except Movement.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        movement = self.get_object(pk)
        serializer = MovementSerializer(movement)
        return Response(serializer.data)

    def delete(self, request, pk):
        movement = self.get_object(pk)
        movement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
