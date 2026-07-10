from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.controllers.supplier_controller import SupplierController
from backend.database import get_db
from backend.services.supplier_service import SupplierService

router = APIRouter()


def controller(db: AsyncSession = Depends(get_db)) -> SupplierController:
    return SupplierController(SupplierService(db))


@router.get("")
async def list_suppliers(c: SupplierController = Depends(controller)):
    pass


@router.get("/{supplier_id}")
async def get_supplier(supplier_id: int, c: SupplierController = Depends(controller)):
    pass
