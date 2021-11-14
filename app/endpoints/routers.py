from fastapi import APIRouter

from app.services import parse

router = APIRouter(tags=["Olx Adds"])


@router.get("/items/{q}")
def list_posts(q: str, currency: str = None, p_from: int = 0, p_to: int = 0):
    """
    ## Retrieve a list of advertisements

    ### Filtering
    #### q:
    what do you want to find </br>
    #### currency:
    USD or EUR (default GRN) </br>
    #### p_from:
    filter price from </br>
    #### p_to:
    filter price to </br>
    """
    return parse.parse(search=q, currency=currency, p_from=p_from, p_to=p_to)
