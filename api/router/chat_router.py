from fastapi import APIRouter
from base import message_item, text_generator_model, LOGGER


chat_router = APIRouter()


@chat_router.post("/chat")
async def chat_to_ai(chat_json: message_item.ChatItem):
    """The function `chat_to_ai` takes a chat message as input, generates a reply using a text generation
    model, and returns the generated reply.

    Parameters
    ----------
    chat_json : message_item.ChatItem
        The parameter `chat_json` is of type `message_item.ChatItem`. It represents a chat message in JSON
    format. It contains the `message` field, which is the text of the chat message.

    Returns
    -------
        The function `chat_to_ai` returns a dictionary with a single key-value pair. The key is "message"
    and the value is the generated reply message from the AI model.

    """
    provider, reply_message = await text_generator_model.generate(
        prompt=chat_json.prompt
    )
    LOGGER.info(f"provider :{provider}")
    return {"message": reply_message}
