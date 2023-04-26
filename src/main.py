from config import SERVER_ID
import server
from blockchain import Node
from gevent import monkey

monkey.patch_all()
if __name__ == '__main__':
    current_node = Node(SERVER_ID)
    server.start(SERVER_ID, current_node)
