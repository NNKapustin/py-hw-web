from uuid import UUID

from sqlalchemy.exc import IntegrityError

from db.db import AsyncSession
from db.models import ORM_MODEL, ORM_MODEL_CLS
from errors import Conflict, NotFound


async def get_item(session: AsyncSession, item_class: ORM_MODEL_CLS, item_id: int | str | UUID) -> ORM_MODEL:
    item = await session.get(item_class, item_id)
    if item is None:
        raise NotFound(f"{item_class.__name__.lower()} not found")
    return item


async def create_item(session: AsyncSession, model_cls: ORM_MODEL_CLS, commit: bool = True, **params) -> ORM_MODEL:
    new_item = model_cls(**params)
    session.add(new_item)
    if commit:
        try:
            await session.commit()
        except IntegrityError as er:
            if er.orig.args and "UniqueViolationError" in er.orig.args[0]:
                raise Conflict(f"such {model_cls.__name__.lower()} already exists")
    return new_item


async def patch_item(session: AsyncSession, item: ORM_MODEL, commit: bool = True, **params) -> ORM_MODEL:
    for field, value in params.items():
        setattr(item, field, value)
    session.add(item)
    if commit:
        try:
            await session.commit()
        except IntegrityError as er:
            if "UniqueViolationError" in er.orig.args[0]:
                raise Conflict(f"such {item.__class__.__name__.lower()} already exists")
    return item


async def delete_item(session: AsyncSession, item: ORM_MODEL, commit: bool = True):
    await session.delete(item)
    if commit:
        await session.commit()
