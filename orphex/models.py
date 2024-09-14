from django.db import models


class AbstractBaseModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        field_names_and_values = [f"{key}={value}" for key, value in self.__dict__.items() if not str(key).startswith("_")]
        return f"{class_name}({", ".join(field_names_and_values)})"


class Status(AbstractBaseModel):
    id = models.SmallAutoField(primary_key=True)
    status = models.TextField(null=False, unique=True)


class Type(AbstractBaseModel):
    id = models.SmallAutoField(primary_key=True)
    type = models.TextField(null=False, unique=True)


class Category(AbstractBaseModel):
    id = models.SmallAutoField(primary_key=True)
    category = models.TextField(null=False, unique=True)


class CustomerConversionRate(AbstractBaseModel):
    id = models.AutoField(primary_key=True)
    customer_id = models.TextField(null=False, unique=True)
    conversions = models.PositiveBigIntegerField(null=False)
    revenues = models.FloatField(null=False)
    rate = models.FloatField(null=False)
