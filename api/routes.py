from fastapi import APIRouter
from fastapi import HTTPException
from models import Part
from actions import action_view_urparts
from typing import List, Optional


router = APIRouter()


@router.get("/parts", response_model=List[Part], tags=["parts"])
async def view_urparts(
    manufacturer: Optional[str] = None,
    category: Optional[str] = None,
    model: Optional[str] = None,
    part: Optional[str] = None,
    part_category: Optional[str] = None
):
    """A route to retrieve machinery parts data
    considering query strings.

    Args:
        manufacturer (str, optional): A manufacturer query. Defaults to None.
        category (str, optional): A category query. Defaults to None.
        model (str, optional): A model query. Defaults to None.
        part (str, optional): A part query. Defaults to None.
        part_category (str, optional): A part categoruy query. Defaults to None.

    Raises:
        HTTPException: Raises an Internal Server Error.

    Returns:
        List[Part]: A list of parts model.
    """
    try:
        return action_view_urparts(
            manufacturer,
            category,
            model,
            part,
            part_category
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Exception: {e}")
