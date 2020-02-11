from .vision import detect_tables, initialize_cams
from .pathfinding import find_next_directions
from aiohttp import json_response
from wirepickle import Client

# this is ONE BACKEND for ONE ROOM -- swap multiple for multiple rooms

async def initialize(request):
    try:
        initialize_cams()
    except e as Exception:
        return json_response({
            error: True,
            message: str(e)
        })
    return json_response({
        error: False
    })

async def get_next_move(request):
    try:
        find_next_directions(request.id)
    except e as Exception:
        return json_response({
            error: True,
            message: str(e)
        })
    return json_response({
        error: False
    })
    

    

