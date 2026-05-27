import hashlib
import json
from time import time


class Block:

    def __init__(self, index, timestamp, data, previous_hash):

        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):

        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


class Blockchain:

    def __init__(self):

        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):

        return Block(
            0,
            time(),
            "Genesis Block",
            "0"
        )

    def get_latest_block(self):

        return self.chain[-1]

    def add_block(self, data):

        latest_block = self.get_latest_block()

        new_block = Block(
            len(self.chain),
            time(),
            data,
            latest_block.hash
        )

        self.chain.append(new_block)

    def update_status(self, block_index, new_status):

        if block_index > 0 and block_index < len(self.chain):

            self.chain[block_index].data['status'] = new_status

    def display_chain(self):

        blockchain_data = []

        for block in self.chain:

            blockchain_data.append({
                "Index": block.index,
                "Timestamp": block.timestamp,
                "Data": block.data,
                "Hash": block.hash,
                "Previous Hash": block.previous_hash
            })

        return blockchain_data