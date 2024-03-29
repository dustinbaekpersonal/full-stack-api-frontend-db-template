"""Schemas of Inventory required as an input of API request."""
from enum import Enum
from typing import List

from pydantic import BaseModel


class AllowedStoreNames(str, Enum):
    """Allowed store names."""

    waitrose = "Waitrose"
    sainsbury = "Sainsbury's"
    aldi = "Aldi"


class AllowedProductNames(str, Enum):
    """Allowed product names."""

    milk = "milk"
    bread = "bread"
    fruit = "fruit"


class ProductNames(BaseModel):
    """Pydantic schema for products."""

    product_name: AllowedProductNames
    stock_level: int
    # updated_at: datetime


class Inventory(BaseModel):
    """Pydantic schema for stores."""

    store_name: AllowedStoreNames
    product_detail: List[ProductNames]


class InventoryDelete(BaseModel):
    """Pydantic schema to be used when to delete inventory record."""

    store_name: AllowedStoreNames
    product_name: AllowedProductNames
