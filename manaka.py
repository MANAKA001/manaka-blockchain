
import hashlib
import json
from datetime import datetime, timezone


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        encoded = json.dumps(
            block_data, sort_keys=True, ensure_ascii=False
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


class ManakaBlockchain:
    def __init__(self):
        self.chain = [
            Block(0, ["MANAKA blockchain created"], "0")
        ]

    def add_block(self, transactions):
        previous = self.chain[-1]
        block = Block(
            len(self.chain), transactions, previous.hash
        )
        self.chain.append(block)
        return block

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

    def show_chain(self):
        for block in self.chain:
            print(json.dumps({
                "index": block.index,
                "timestamp": block.timestamp,
                "transactions": block.transactions,
                "previous_hash": block.previous_hash,
                "hash": block.hash,
            }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    manaka = ManakaBlockchain()
    manaka.add_block([
        {"from": "KARO", "to": "MANAKA", "amount": 100}
    ])

    print("=== MANAKA BLOCKCHAIN ===")
    manaka.show_chain()
    print("Blockchain valid:", manaka.is_valid())
