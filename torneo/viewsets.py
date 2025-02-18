from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Torneo
from .serializers import TorneoSerializer, TorneoSerializerCreate, TorneoSerializerActualizarNombre

class TorneoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los torneos con operaciones CRUD completas.
    """
    queryset = Torneo.objects.all()

    def get_serializer_class(self):
        """
        Selecciona el serializer según la acción que se está ejecutando.
        """
        if self.action == 'create':  # POST
            return TorneoSerializerCreate
        elif self.action == 'partial_update':  # PATCH
            return TorneoSerializerActualizarNombre
        return TorneoSerializer  # GET, PUT, DELETE

    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo torneo con validaciones personalizadas.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Torneo creado correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Edita completamente un torneo.
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Actualiza parcialmente un torneo (ej. solo el nombre).
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Elimina un torneo y devuelve una respuesta personalizada.
        """
        instance = self.get_object()
        instance.delete()
        return Response({"mensaje": "Torneo eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
