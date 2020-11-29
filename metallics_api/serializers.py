from rest_framework import serializers
from django.forms.models import model_to_dict
from .models import Chemical, Commodity, Composition


class ChemicalCompositionSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = CompositionSerializer(value)
        data = serializer.data
        result = {}
        for k, v in data.items():
            if k == "element":
                result["element"] = model_to_dict(Chemical.objects.get(id=v))
            elif k == "percentage":
                result["percentage"] = v
            else:
                pass
        return result


class ChemicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chemical
        fields = ("id", "name")


class CompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composition
        fields = ("id", "commodity", "element", "percentage")


class CommoditySerializer(serializers.ModelSerializer):
    chemical_composition = ChemicalCompositionSerializer(source="composition_set", many=True, read_only=True)

    class Meta:
        model = Commodity
        fields = ("id", "name", "price", "inventory", "chemical_composition")
