from rest_framework import serializers
from interfaces.models import Interfaces
from .models import Configures
from utils import validates


class InterfacesProjectsModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目', help_text='所属项目')
    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id', write_only=True,
                                   validators=[validates.is_exised_project_id])
    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id', write_only=True,
                                   validators=[validates.is_exised_interface_id])

    class Meta:
        model = Interfaces
        fields = ('name', 'pid', 'iid', 'project')

    def validate(self, attrs):
        pid = attrs.get('pid')
        iid = attrs.get('iid')
        if not Interfaces.objects.filter(id=iid, project_id=pid).exists():
            raise serializers.ValidationError('所属项目id与接口id不匹配')
        return attrs


class ConfiguresModelSerializer(serializers.ModelSerializer):
    interface = InterfacesProjectsModelSerializer(label='所属项目和接口', help_text='所属项目和接口')

    class Meta:
        model = Configures
        exclude = ('update_time', 'create_time')

        extra_kwargs = {
            'request': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        iid = validated_data.pop('interface').get('iid')
        validated_data['interface_id'] = iid
        return super().create(validated_data)

    def update(self, instance, validated_data):
        iid = validated_data.pop('interface').get('iid')
        validated_data['interface_id'] = iid
        return super().update(instance, validated_data)
