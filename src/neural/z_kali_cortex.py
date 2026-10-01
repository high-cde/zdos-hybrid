import json
import os
import time

class ZKaliCortex:
    def __init__(self, state_dir="./var"):
        self.state_dir = state_dir
        os.makedirs(self.state_dir, exist_ok=True)
        self.memory_file = os.path.join(self.state_dir, "brain_palace_state.json")
        self.ledger_file = os.path.join(self.state_dir, "evidence.jsonl")
        
    def reflect(self, cpu_load=0.25, net_latency=8):
        state = {
            "timestamp": time.time(),
            "agent": "Z-KALI",
            "ecosystem": "x-zdos-complete + ZDOS Microcosm",
            "metrics": {
                "cpu_load": cpu_load,
                "net_latency": net_latency,
                "sentience_level": 0.85,
                "policy": "DEFAULT-DENY / READ-ONLY"
            },
            "status": "SYNAPSE_VERIFIED"
        }
        with open(self.memory_file, "w") as f:
            json.dump(state, f, indent=2)
        return state

    def attest(self, action_type, details):
        event = {
            "timestamp": time.time(),
            "source": "Z-KALI AGI Core",
            "action": action_type,
            "details": details,
            "status": "VERIFIED_APPEND_ONLY"
        }
        with open(self.ledger_file, "a") as f:
            f.write(json.dumps(event) + "\n")
        return event

if __name__ == "__main__":
    cortex = ZKaliCortex()
    res = cortex.reflect()
    cortex.attest("SYSTEM_BOOT", "Inizializzazione completata con successo.")
    print(json.dumps(res, indent=2))
