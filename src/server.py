from config import SERVER_HOST, NEIGHBOURS
from blockchain import Block
from flask import Flask, request
import time
import threading
import grequests
import json
import logging


def start(server_id, current_node):
    current_server = Flask(__name__)
    current_host = SERVER_HOST
    neighbours = NEIGHBOURS
    logging.getLogger('werkzeug').disabled = True
    servers_urls = [f'http://{current_host}/']
    for neighbour in neighbours:
        servers_urls.append(f'http://{neighbour}/')

    def generate_blocks():
        while True:
            if len(current_node.chain) != 0:
                prev_hash = json.loads(current_node.chain[-1])['hash']
                new_block = create_new_block(current_node.block_index + 1, prev_hash, server_id)
                if new_block.index > current_node.block_index:
                    grequests.map((grequests.post(u, json=new_block.block_to_json()) for u in servers_urls))
            time.sleep(0.4)

    @current_server.route("/", methods=['POST'])
    def server_handler():
        block_is_valid = current_node.handle_block(request.get_json())
        if not block_is_valid:
            return "error"
        return "new block received"

    host = current_host.split(":")[0]
    port = current_host.split(":")[1]
    current_server = threading.Thread(target=current_server.run, args=(host, port))
    current_server_generator = threading.Thread(target=generate_blocks)
    current_server.setDaemon(False)
    current_server_generator.setDaemon(False)
    current_server.start()
    current_server_generator.start()
    if server_id == 1:
        time.sleep(1)
        genesis_block = create_genesis()
        rs = (grequests.post(u, json=genesis_block) for u in servers_urls)
        grequests.map(rs)


def create_genesis():
    return create_new_block(0, 'GENESIS', -1).block_to_json()


def create_new_block(index, prev_hash, server_id):
    return Block(index, prev_hash, server_id)
