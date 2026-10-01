import subprocess
import json
import os
from src.neural.z_kali_cortex import ZKaliCortex

def main():
    print("🧬 [Z-KALI] Inizializzazione del ciclo sinaptico integrato...")
    
    # 1. Esegue il binario dell'organismo in Rust per un singolo battito
    res = subprocess.run(
        ["target/debug/organism-bin", "--once"],
        capture_output=True,
        text=True,
        env={**os.environ, "ZDOS_STATE_DIR": "./var", "ZDOS_LLM_URL": "http://127.0.0.1:8080/llm"}
    )
    
    print("--- OUTPUT ORGANISM-BIN ---")
    print(res.stdout.strip())
    
    # 2. Attiva il Cortex di Z-KALI ereditando la memoria di Brain Palace
    cortex = ZKaliCortex(state_dir="./var")
    synapse_state = cortex.reflect(cpu_load=0.42, net_latency=12)
    
    print("--- SYNAPSE MEMORY STATE ---")
    print(json.dumps(synapse_state, indent=2))
    print("✨ [Z-KALI] Ciclo completato con successo. Memoria persistita.")

if __name__ == "__main__":
    main()
