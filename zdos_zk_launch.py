#!/usr/bin/env python3
import subprocess
import sys
import time
from pathlib import Path

root = Path("/home/ruby/zdos-organism")
os_path = root / "zdos_omni_os.py"
microcosm_dir = root / "zdos-microcosm-beta"

print("==================================================")
print("  ZDOS HYBRID SECURITY WORKSTATION (Parrot Edition)")
print("  Integrazione: ZComm, Evidence Chain, Node Pulse")
print("==================================================")

server_process = None
node_script = microcosm_dir / "node" / "zdos-node.ts"
if node_script.exists():
    print("[*] Avvio ZDOS Node Pulse in background (porta 8787)...")
    try:
        server_process = subprocess.Popen(
            ["npx", "tsx", "node/zdos-node.ts"],
            cwd=str(microcosm_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"[!] Avviso avvio background node: {e}")

time.sleep(1)

try:
    if os_path.exists():
        print("[*] Apertura ZDOS Glass Engine (Parrot Security Interface)...")
        subprocess.run([sys.executable, str(os_path)], cwd=str(root))
    else:
        print(f"[!] Errore: {os_path} non trovato.")
except KeyboardInterrupt:
    print("\n[!] Interruzione utente.")
finally:
    if server_process:
        print("[*] Chiusura servizi in background...")
        server_process.terminate()
        server_process.wait()
    print("[*] Sessione ZDOS conclusa in sicurezza.")
