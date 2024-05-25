import json
from aiohttp import web
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext,
    MessageFactory
)
import asyncio

# Initialize adapter with None credentials for local testing
adapter_settings = BotFrameworkAdapterSettings(None, None)
adapter = BotFrameworkAdapter(adapter_settings)

# Store user state
user_state = {}

async def messages(req):
    body = await req.json()
    activity = Activity().deserialize(body)
    
    async def turn_handler(turn_context: TurnContext):
        user_id = turn_context.activity.from_property.id
        if user_id not in user_state:
            user_state[user_id] = {}
        
        user_data = user_state[user_id]
        user_message = turn_context.activity.text.lower()
        
        if "name" not in user_data:
            user_data["name"] = None

        if user_data["name"] is None:
            user_data["name"] = user_message
            bot_reply = f"Nice to meet you, {user_data['name']}! How are you today?"
        elif user_message in ["hi", "hello", "hey"]:
            bot_reply = f"Hello {user_data['name']}! How can I assist you today?"
        elif "how are you" in user_message:
            bot_reply = "I'm just a bot, but I'm here to help you! How can I assist you?"
        elif user_message in [ "i am good", "i am fine"]:
            bot_reply = "Good to hear. I am also having wonderful day. "

        else:
            bot_reply = "I'm not sure I understand you fully. Can you tell me more?"

        reply = MessageFactory.text(bot_reply)
        await turn_context.send_activity(reply)
    
    await adapter.process_activity(activity, "", turn_handler)
    return web.Response(text="", status=200)

app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=3978)
