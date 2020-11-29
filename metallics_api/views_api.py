from rest_framework import viewsets
from .models import Chemical, Composition, Commodity
from .serializers import ChemicalSerializer, CompositionSerializer, CommoditySerializer
from rest_framework.permissions import IsAuthenticated

class ChemicalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer

class CommodityViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer

class CompositionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer