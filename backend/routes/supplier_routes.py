from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.supplier_controller import SupplierController
from backend.database import get_db
from backend.schemas.supplier import SupplierOut
from backend.services.supplier_service import SupplierService

router = APIRouter()


def controller(db: AsyncSession = Depends(get_db)) -> SupplierController:
    return SupplierController(SupplierService(db))


@router.get("", response_model=list[SupplierOut])
async def list_suppliers(c: SupplierController = Depends(controller)):
    return await c.index()


@router.get("/{supplier_id}", response_model=SupplierOut)
async def get_supplier(supplier_id: int, c: SupplierController = Depends(controller)):
    return await c.show(supplier_id)
