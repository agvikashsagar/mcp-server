# ClickHouse Chatbot MCP (No LLM)

A lightweight chatbot server that connects to ClickHouse and answers basic queries 
like listing databases, listing tables, and counting rows in a table.  
Runs entirely inside your network — no external AI required.

## 🚀 Setup

```bash
git clone <your-repo-url>
cd clickhouse-chatbot
pip install -r requirements.txt

## RUN

python chatbot_server.py

Server will start at: 	
ws://localhost:8765

Send JSON-RPC messages via WebSocket:

{"jsonrpc":"2.0","id":1,"params":{"message":"list databases"}}


Response:

{"jsonrpc":"2.0","id":1,"result":"Databases: default, system, mydb"}

🛠 Extend Intents

Edit config.yaml to add new intents:

- pattern: "top 10 from"
  sql: "SELECT * FROM {table} LIMIT 10"
  format: "list"


Restart the server to apply changes.




