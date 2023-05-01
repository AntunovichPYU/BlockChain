import os

SERVER_ID = int(os.environ.get("SERVER_ID", 1))
SERVER_HOST = os.environ.get("SERVER_HOST", "node1:5000")
NEIGHBOURS = os.environ.get("NEIGHBOURS", "node2:5001,node3:5002").split(",")
