import asyncio
import json
from clickhouse_driver import Client
import websockets
import re
import yaml

# Load config (intents → SQL)
with open("config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

# 🔹 Connect to ClickHouse
client = Client(host="localhost")  # change host/user/password/db

def handle_query(user_input: str) -> str:
    user_input = user_input.lower().strip()

    try:
        # Go through configured intents
        for intent in CONFIG["intents"]:
            if re.search(intent["pattern"], user_input):
                query = intent["sql"]

                # If query has placeholder {table}, replace with table name from input
                if "{table}" in query and "table" in user_input:
                    table_name = user_input.split("table")[-1].strip()
                    query = query.replace("{table}", table_name)

                result = client.execute(query)

                # Format result
                if intent.get("format") == "list":
                    return ", ".join([row[0] for row in result])
                elif intent.get("format") == "count":
                    return f"{result[0][0]}"
                else:
                    return str(result)

        return "Sorry, I don’t understand. Try: list databases, list tables <db>, count rows in table <name>."

    except Exception as e:
        return f"Error: {str(e)}"

# 🔹 JSON-RPC over WebSocket
async def handle_client(websocket):
    async for message in websocket:
        request = json.loads(message)
        user_input = request.get("params", {}).get("message", "")

        response_text = handle_query(user_input)

        response = {
            "jsonrpc": "2.0",
            "result": response_text,
            "id": request.get("id")
        }
        await websocket.send(json.dumps(response))

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("✅ ClickHouse chatbot server running at ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

