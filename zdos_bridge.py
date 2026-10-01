import json
import os
import time

class ZDOSPtoAGIBridge:
    def __init__(self, state_dir="./var"):
        self.state_dir = state_dir
        os.makedirs(self.state_dir, exist_ok=True)
        self.ledger_path = os.path.join(self.state_dir, "evidence.jsonl")

    def attest_state(self, agent_name, metric_status):
        event = {
            "timestamp": time.time(),
            "source": agent_name,
            "target": "ZDOS Microcosm / Evidence Chain",
            "status": metric_status,
            "policy": "DEFAULT-DENY / READ-ONLY"
        }
        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(event) + "\n")
        return event

if __name__ == "__main__":
    bridge = ZDOSPtoAGIBridge()
    res = bridge.attest_state("Z-KALI", "SYNC_VERIFIED")
    print("🔗 [ZDOS-BRIDGE] Evento attestato nel ledger locale:", json.dumps(res, indent=2))
