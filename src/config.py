import os

SERVER_ID = int(os.environ.get("SERVER_ID", 1))
SERVER_HOST = os.environ.get("SERVER_HOST", "localhost")
PORT_1 = int(os.environ.get("PORT_1", 5000))
PORT_2 = int(os.environ.get("PORT_2", 5001))
PORT_3 = int(os.environ.get("PORT_3", 5002))
