from rest_framework import serializers

from apps.products.models import OptionValue, Option


class AddOptionValueSerializer(serializers.ModelSerializer):
    option = serializers.CharField(write_only=True)

    class Meta:
        model = OptionValue
        fields = (
            "id",
            "option",
            "value"
        )

    def create(self, validated_data):
        option_name = validated_data.pop("option")
        try:
            option = Option.objects.get(name=option_name)
        except Option.DoesNotExist:
            raise serializers.ValidationError({"option": "Option with this name does not exist."})
        except Option.MultipleObjectsReturned:
            raise serializers.ValidationError({"Course": "Bunday nomda bir nechta kurs mavjud, aniq nom kiriting."})
        
                
        value = OptionValue.objects.create(option=option, **validated_data)
        return value