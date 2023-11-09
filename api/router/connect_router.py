from fastapi import APIRouter
from base import monitor_micro_server, ConnectPlugItem, LOGGER

connect_api_router = APIRouter()


@connect_api_router.post("/connect")
async def connect_plug(connect_plug_item: ConnectPlugItem):
    """The function `connect_plug` adds a new micro server to the `monitor_micro_server` and logs the
    details.

    Parameters
    ----------
    connect_plug_item : ConnectPlugItem
        The parameter `connect_plug_item` is of type `ConnectPlugItem`.

    Returns
    -------
        a dictionary with a single key-value pair. The key is "message" and the value is "OK".

    """
    monitor_micro_server.add_micro_server(
        micro_server_name=connect_plug_item.type_name,
        micro_server_url=connect_plug_item.url,
        micro_server_is_alive_root=connect_plug_item.check_alive_root,
    )
    LOGGER.info(
        f"add new service, name: {connect_plug_item.type_name} , url: {connect_plug_item.url}"
    )
    return {"message": "OK"}


@connect_api_router.get("/connect")
async def display_micro_service():
    """The function `display_micro_service` returns all microservices monitored by `monitor_micro_server`.

    Returns
    -------
        the result of the `get_all_micro_service()` method call from the `monitor_micro_server` object.

    """
    return monitor_micro_server.get_all_micro_service()


@connect_api_router.get("/connect_format")
async def display_micro_service():
    """The function `display_micro_service` returns a dictionary containing information about a
    microservice, including its type, URL, and a root endpoint for checking if the service is alive.

    Returns
    -------
        A dictionary containing format about a micro service.

    """
    return {
        "type_name": "type of provide service",
        "url": "service server URL",
        "check_alive_root": "for sever to check the service is alive",
    }
