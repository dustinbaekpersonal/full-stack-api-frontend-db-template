"""API calls for inventory are defined."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.items import Product, Store
from app.schemas.items import Inventory, InventoryDelete

router = APIRouter(prefix="/inventory")


db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.get("/{store_name}")
async def fetch_product_by_store_id(store_name: str, db: db_dependency):
    """Fetch product's stock level by store name.

    Args:
        store_name (str): name of the stores.
        db (AsyncSession): single logical asynchronous database transaction.
    """
    # retrieve Store model instance (i.e. row in stores table) given store name
    store = await Store.search(store_name, db)

    if not store:
        # when there isn't store_name in stores table in db
        raise HTTPException(status_code=404, detail=f"Store '{store_name}' not found.")
    logger.info(f"Store with store name: {store_name} has {store}")

    # retrieve Product model instance using store id
    products = await Product.search_by_store(store.id, db)

    if not products:
        raise HTTPException(
            status_code=404,
            detail=f"Store {store_name} does not have any inventory.",
        )

    return products


### helper function to create store and inventory for the first time ###
async def create_inventory(inventory: Inventory, db: db_dependency):
    """Create store and product object in Postgresql database.

    Args:
        inventory (Inventory): pydantic schema of Inventory defining user input.
        db (AsyncSession): single logical asynchronous database transaction.
    """
    # create an instance of Store with store_name
    db_store = Store(store_name=inventory.store_name)
    await db_store.create(db)

    # for each product, create Product model instance and add to products table
    for product in inventory.product_detail:
        db_product = Product(
            product_name=product.product_name,
            stock_level=product.stock_level,
            store_id=db_store.id,
        )
        db.add(db_product)
    await db.commit()


@router.put("/")
async def update_inventory(inventory: Inventory, db: db_dependency):
    """Update stock level of given product and store.

    Args:
        inventory (Inventory): pydantic schema of Inventory
        db (AsyncSession): single logical asynchronous database transaction.
    """
    store_name = inventory.store_name
    # Check if the store exists
    store = await Store.search(store_name, db)

    if not store:
        logger.info(f"Store '{store_name}' not found. Create store first.")
        return await create_inventory(inventory, db)

    for product_info in inventory.product_detail:
        # Check if the product exists for the given store
        product = await Product.search_by_store_product_name(
            store.id, product_info.product_name, db
        )

        if not product:
            logger.info(
                f"Product '{product_info.product_name}' not found "
                + f"for store '{store_name}'."
            )
            logger.info("Populating product...")
            db_product = Product(
                product_name=product_info.product_name,
                stock_level=product_info.stock_level,
                store_id=store.id,
            )
            db.add(db_product)
            continue

        # Update stock level
        product.stock_level = product_info.stock_level

    await db.commit()


@router.delete("/")
async def delete_inventory(inventory: InventoryDelete, db: db_dependency):
    """Delete inventory record in Products table.

    Args:
        inventory (InventoryDelete): pydantinc schema to define to delete record
        db (AsyncSession): single logical asynchronous database transaction
    """
    store_name = inventory.store_name
    product_name = inventory.product_name

    # Check if the store exists
    store = await Store.search(store_name, db)

    product = await Product.search_by_store_product_name(store.id, product_name, db)

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_name} does not exist for store {store_name}.",
        )

    return await product.delete(db)
