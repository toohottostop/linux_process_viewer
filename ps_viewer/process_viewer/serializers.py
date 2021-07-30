from rest_framework import serializers
from process_viewer.models import PsValues


class PsValuesListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        data_mapping = {item['pid']: item for item in validated_data}
        objects = []
        for pid, data in data_mapping.items():
            value = PsValues.objects.filter(pid=pid).first()
            if value is None:
                objects.append(self.child.create(data))
            else:
                objects.append(self.child.update(value, data))
        return objects


class PsValuesSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = PsValuesListSerializer
        model = PsValues
        fields = ['id', 'pid', 'cpu_usage', 'memory_usage', 'command']
