from fastapi import APIRouter
from base import message_item, text_generator_model, LOGGER


chat_router = APIRouter()


@chat_router.post("/chat")
async def chat_to_ai(chat_json: message_item.ChatItem):
    """
    The function `chat_to_ai` takes a JSON object representing a chat message, generates a reply using a
    text generation model, and returns the reply as a JSON object.

    :param chat_json: The `chat_json` parameter is a JSON object that contains information about the
    chat message. It typically includes the message content and any other relevant details such as the
    sender's name or ID
    :type chat_json: ChatItem
    :return: a dictionary with a single key-value pair. The key is "message" and the value is the
    generated reply message from the AI model.
    """
    provider, reply_message = await text_generator_model.generate(
        prompt=chat_json.message
    )
    LOGGER.info(f"provider :{provider}")
    return {"message": reply_message}
