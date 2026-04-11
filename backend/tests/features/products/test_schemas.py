"""Tests for products Pydantic schemas."""

import uuid
from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.features.products.schemas import (
    ImageCreate,
    ImageReorder,
    ProductCreate,
    ProductUpdate,
    VariantCreate,
    VariantUpdate,
)


def test_product_create_valid():
    p = ProductCreate(line="polo_atelier", name="Polo Test")
    assert p.line == "polo_atelier"
    assert p.description is None


def test_product_create_invalid_line():
    with pytest.raises(ValidationError):
        ProductCreate(line="invalid_line", name="X")


def test_variant_create_valid():
    v = VariantCreate(
        style="classic",
        size="M",
        color="Black",
        cost_acquisition_usd=Decimal("50.00"),
        price_usd=Decimal("120.00"),
    )
    assert v.stock_qty == 0


def test_variant_create_invalid_size():
    with pytest.raises(ValidationError):
        VariantCreate(
            style="classic",
            size="XXS",
            color="Black",
            cost_acquisition_usd=Decimal("50.00"),
            price_usd=Decimal("120.00"),
        )


def test_product_update_all_none_allowed():
    u = ProductUpdate()
    assert u.name is None and u.description is None and u.is_active is None


def test_image_reorder_requires_list():
    ids = [uuid.uuid4(), uuid.uuid4()]
    r = ImageReorder(image_ids=ids)
    assert len(r.image_ids) == 2
