from rest_framework import serializers

from orphex.models import CustomerPerformance, PerformanceDistribution


class ConversionRateSerializer(serializers.ModelSerializer):
    rate = serializers.FloatField(source="conversion_rate")

    class Meta:
        model = CustomerPerformance
        fields = ["customer_id", "rate"]


class ConversionRatesSerializer(serializers.Serializer):
    conversion_rates = serializers.ListField()
    min_rate = serializers.SerializerMethodField(required=False)
    max_rate = serializers.SerializerMethodField(required=False)

    def get_min_rate(self, obj):
        return obj["conversion_rates"][0]["rate"] if len(obj["conversion_rates"]) > 0 else None

    def get_max_rate(self, obj):
        return obj["conversion_rates"][-1]["rate"] if len(obj["conversion_rates"]) > 0 else None


class StatusDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceDistribution
        fields = "status", "type", "category", "total_revenue", "total_conversions"


class CategoryTypePerformanceSerializer(serializers.Serializer):
    type = serializers.CharField()
    category = serializers.CharField()
    total_revenue = serializers.FloatField()
    total_conversions = serializers.IntegerField()


class CategoryTypePerformancesSerializer(serializers.Serializer):
    category_and_type_performances = serializers.ListField()
    top_performing_category = serializers.CharField(required=False)
    top_performing_type = serializers.CharField(required=False)

    def get_top_performing_category(self, obj):
        return obj["category_and_type_performances"][0]["category"] if len(obj["category_and_type_performances"]) > 0 else None

    def get_top_performing_type(self, obj):
        return obj["category_and_type_performances"][0]["type"] if len(obj["category_and_type_performances"]) > 0 else None


class FilteredAverageCustomerPerformanceDistributionSerializer(serializers.Serializer):
    customer_id = serializers.CharField()
    average_revenue = serializers.FloatField()
    average_conversions = serializers.FloatField()
