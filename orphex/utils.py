from django.db import models


def model_to_string(self: models.Model) -> str:
    class_name = self.__class__.__name__
    field_names_and_values = [f"{key}={value}" for key, value in self.__dict__.items() if not str(key).startswith("_")]
    return f"{class_name}({", ".join(field_names_and_values)})"
