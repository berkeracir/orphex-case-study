from rest_framework import serializers

from orphex.models import CustomerConversionRate


class ConversionRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerConversionRate
        fields = ["customer_id", "rate"]


class ConversionRatesSerializer(serializers.Serializer):
    conversion_rates = serializers.ListField()
    min_rate = serializers.SerializerMethodField(required=False)
    max_rate = serializers.SerializerMethodField(required=False)

    def get_min_rate(self, obj):
        return obj["conversion_rates"][0]["rate"] if len(obj["conversion_rates"]) > 0 else None

    def get_max_rate(self, obj):
        return obj["conversion_rates"][-1]["rate"] if len(obj["conversion_rates"]) > 0 else None
