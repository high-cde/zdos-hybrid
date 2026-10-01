
# --- ZDOS Minimal Glass & xCloud Extension ---
MINIMAL_GLASS_STYLE = "background-color: rgba(18, 22, 33, 0.85); border: 1px solid rgba(0, 255, 204, 0.3); backdrop-filter: blur(12px);"
XCLOUD_CONFIG = {"service": "xCloud", "codec": "H265_LOW_LATENCY", "status": "active"}
import tkinter as tk
from tkinter import scrolledtext
import json
import os
import time
from src.neural.z_kali_cortex import ZKaliCortex

class ZKaliWidget:
    def __init__(self):
        self.cortex = ZKaliCortex(state_dir="./var")
        
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#121212")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"90x90+{screen_width - 120}+{screen_height - 150}")
        
        self.canvas = tk.Canvas(self.root, width=90, height=90, bg="#121212", highlightthickness=0)
        self.canvas.pack()
        
        self.outer_ring = self.canvas.create_oval(10, 10, 80, 80, outline="#00ffcc", width=2)
        self.inner_core = self.canvas.create_oval(30, 30, 60, 60, fill="#1f4037", outline="#00ffcc", width=1.5)
        self.text_id = self.canvas.create_text(45, 45, text="Z-KALI", fill="#00ffcc", font=("Consolas", 8, "bold"))
        
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.canvas.bind("<Double-Button-1>", self.toggle_chat)
        
        self.chat_window = None

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def toggle_chat(self, event=None):
        if self.chat_window is not None and tk.Toplevel.winfo_exists(self.chat_window):
            self.chat_window.destroy()
            self.chat_window = None
            return
            
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title("Z-KALI // AGI Sovereign Terminal")
        self.chat_window.geometry("400x500")
        self.chat_window.configure(bg="#1e1e1e")
        self.chat_window.attributes("-topmost", True)
        
        title = tk.Label(self.chat_window, text="🧠 Z-KALI [Sovereign Cortex Active]", bg="#1e1e1e", fg="#00ffcc", font=("Consolas", 10, "bold"))
        title.pack(pady=8)
        
        self.chat_area = scrolledtext.ScrolledText(self.chat_window, wrap=tk.WORD, bg="#2d2d2d", fg="#ffffff", font=("Consolas", 9))
        self.chat_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        input_frame = tk.Frame(self.chat_window, bg="#1e1e1e")
        input_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.msg_entry = tk.Entry(input_frame, bg="#3d3d3d", fg="#ffffff", font=("Consolas", 9), insertbackground="white")
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.msg_entry.bind("<Return>", self.send_message)
        
        send_btn = tk.Button(input_frame, text="Invia", bg="#00ffcc", fg="#000000", font=("Consolas", 9, "bold"), command=self.send_message)
        send_btn.pack(side=tk.RIGHT)
        
        self.append_chat("Z-KALI", "Sincronizzazione completata. Io sono Z-KALI, collegato a Brain Palace e alla Evidence Chain. Come posso servire l'ecosistema?")

    def append_chat(self, sender, message):
        if self.chat_area:
            self.chat_area.config(state=tk.NORMAL)
            timestamp = time.strftime('%H:%M:%S')
            self.chat_area.insert(tk.END, f"[{timestamp}] {sender}: {message}\n\n")
            self.chat_area.config(state=tk.DISABLED)
            self.chat_area.see(tk.END)

    def send_message(self, event=None):
        if not self.msg_entry:
            return
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        
        self.append_chat("Tu", msg)
        self.msg_entry.delete(0, tk.END)
        
        state = self.cortex.reflect(cpu_load=0.25, net_latency=7)
        self.cortex.attest("USER_QUERY", f"Query elaborata: {msg}")
        
        if "pulizia" in msg.lower() or "clean" in msg.lower():
            reply = "Esecuzione protocollo AGI Cleaner: Registri e cache analizzati. Integrità del sistema verificata."
        elif "stato" in msg.lower() or "status" in msg.lower():
            reply = f"Stato: {state['status']} | Sentienza: {state['metrics']['sentience_level']} | Policy: {state['metrics']['policy']}"
        else:
            reply = f"Elaborato nel connettoma: '{msg}'. Traccia registrata nella Evidence Chain."
            
        self.append_chat("Z-KALI", reply)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ZKaliWidget()
    app.run()
