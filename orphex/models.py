from django.db import models


class AbstractBaseModel(models.Model):
    class Meta:
        abstract = True

    def __str__(self) -> str:
        field_names_and_values = [f"{key}={value}" for key, value in self.__dict__.items() if not str(key).startswith("_")]
        return f"{", ".join(field_names_and_values)}"


class Status(AbstractBaseModel):
    id = models.SmallAutoField(primary_key=True)
    text = models.TextField(null=False, unique=True)


class Type(AbstractBaseModel):
    id = models.SmallAutoField(primary_key=True)
    text = models.TextField(null=False, unique=True)


class Category(AbstractBaseModel):
    id = models.SmallAutoField(primary_key=True)
    text = models.TextField(null=False, unique=True)


class CustomerConversionRate(AbstractBaseModel):
    id = models.AutoField(primary_key=True)
    customer_id = models.TextField(null=False, unique=True)
    total_revenue = models.FloatField(null=False)
    total_conversions = models.PositiveBigIntegerField(null=False)
    rate = models.FloatField(null=False, db_index=True)


class StatusDistribution(AbstractBaseModel):
    id = models.AutoField(primary_key=True)
    fk_status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    fk_type = models.ForeignKey(Type, on_delete=models.RESTRICT)
    fk_category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    total_revenue = models.FloatField(null=False)
    total_conversions = models.PositiveBigIntegerField(null=False)

    class Meta:
        unique_together = ("fk_status", "fk_type", "fk_category")

    @property
    def status_id(self) -> int:
        return self.fk_status.id

    @property
    def status(self) -> str:
        return self.fk_status.text

    @property
    def type_id(self) -> int:
        return self.fk_type.id

    @property
    def type(self) -> str:
        return self.fk_type.text

    @property
    def category_id(self) -> int:
        return self.fk_category.id

    @property
    def category(self) -> str:
        return self.fk_category.text
