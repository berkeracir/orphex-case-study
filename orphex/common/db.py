import logging
from typing import List

from orphex.models import Status, Type, Category


logger = logging.getLogger("orphex.common.db")


def create_or_update_statuses(statuses: List[str]) -> List[Status]:
    """Creates or updates Status models

    Args:
        statuses (List[str]): List of statuses as strings

    Returns:
        List[Status]: List of created or updated Status models
    """
    if len(statuses) == 0:
        return []

    result = Status.objects.bulk_create(
        [Status(text=status) for status in statuses], update_conflicts=True, update_fields=["text"], unique_fields=["text"]
    )
    return result


def create_or_update_types(types: List[str]) -> List[Type]:
    """Creates or updates Type models

    Args:
        types (List[str]): List of types as strings

    Returns:
        List[Type]: List of created or updated Type models
    """
    if len(types) == 0:
        return []

    result = Type.objects.bulk_create(
        [Type(text=type) for type in types], update_conflicts=True, update_fields=["text"], unique_fields=["text"]
    )
    return result


def create_or_update_categories(categories: List[str]) -> List[Category]:
    """Creates or updates Category models

    Args:
        categories (List[str]): List of categories as strings

    Returns:
        List[Category]: List of created or updated Category models
    """
    if len(categories) == 0:
        return []

    result = Category.objects.bulk_create(
        [Category(text=category) for category in categories],
        update_conflicts=True,
        update_fields=["text"],
        unique_fields=["text"],
    )
    return result
