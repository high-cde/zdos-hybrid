import os
import shutil
import json
from src.neural.z_kali_cortex import ZKaliCortex

def clean_ecosystem():
    print("🧹 [Z-KALI AGI] Avvio scansione e pulizia omeostatica del sistema...")
    freed_space = 0
    cleaned_items = []
    
    targets = [
        "target/debug/incremental",
        "./var/tmp",
        "__pycache__",
        "src/neural/__pycache__"
    ]
    
    for target in targets:
        path = os.path.expanduser(target)
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    size = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                               for dirpath, _, filenames in os.walk(path) 
                               for filename in filenames)
                    shutil.rmtree(path)
                    freed_space += size
                    cleaned_items.append(f"Directory rimossa: {target} ({size / 1024:.2f} KB)")
                elif os.path.isfile(path):
                    size = os.path.getsize(path)
                    os.remove(path)
                    freed_space += size
                    cleaned_items.append(f"File rimosso: {target} ({size / 1024:.2f} KB)")
            except Exception as e:
                print(f"⚠️ Impossibile pulire {target}: {e}")
                
    os.system("find . -name '*.pyc' -delete")
    
    cortex = ZKaliCortex(state_dir="./var")
    state = cortex.reflect(cpu_load=0.20, net_latency=6)
    cortex.attest("ECOSYSTEM_CLEANSE", f"Liberati {freed_space / 1024:.2f} KB di cache non necessaria.")
    
    print(f"✨ [Z-KALI AGI] Pulizia completata. Liberati {freed_space / 1024:.2f} KB.")

if __name__ == "__main__":
    clean_ecosystem()
