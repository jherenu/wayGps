from rest_framework import viewsets
from .models import Movil
from .serializers import MovilSerializer


class MovilViewSet(viewsets.ModelViewSet):
    queryset = Movil.objects.all()
    serializer_class = MovilSerializer