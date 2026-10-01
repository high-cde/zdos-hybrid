import tkinter as tk
from tkinter import scrolledtext
import time
import random
import os
from src.neural.z_kali_cortex import ZKaliCortex

class ZKaliMegaDriveApp:
    def __init__(self):
        self.cortex = ZKaliCortex(state_dir="./var")
        
        self.root = tk.Tk()
        self.root.title("NEO-CAT // AMSTERDAM '92 (Z-KALI Core)")
        self.root.geometry("640x480")
        self.root.configure(bg="#08041B")
        self.root.attributes("-topmost", True)
        
        self.canvas = tk.Canvas(self.root, width=640, height=260, bg="#0D0A22", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH)
        
        self.draw_scenery(night_mode=True)
        
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg="#06031A", fg="#15E0ED", font=("Courier New", 9), insertbackground="white")
        self.chat_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        input_frame = tk.Frame(self.root, bg="#08041B")
        input_frame.pack(padx=10, pady=8, fill=tk.X)
        
        self.msg_entry = tk.Entry(input_frame, bg="#16123F", fg="#15E0ED", font=("Courier New", 10), insertbackground="white")
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.msg_entry.bind("<Return>", self.send_message)
        
        send_btn = tk.Button(input_frame, text="▶ INVIA", bg="#16123F", fg="#15E0ED", font=("Courier New", 9, "bold"), command=self.send_message)
        send_btn.pack(side=tk.RIGHT)
        
        self.append_chat("Z-KALI", "NEO-CAT AMSTERDAM '92 // Connessione stabilita. Digita un comando o chatta con me.")
        
        self.frame_count = 0
        self.raindrops = [[random.randint(0, 640), random.randint(0, 260)] for _ in range(40)]
        self.animate_scene()

    def draw_scenery(self, night_mode=True):
        self.canvas.delete("all")
        bg_color = "#05020F" if night_mode else "#00B8DB"
        moon_color = "#EAF6FF" if night_mode else "#FFC857"
        
        self.canvas.create_rectangle(0, 0, 640, 260, fill=bg_color, outline="")
        self.canvas.create_oval(520, 30, 570, 80, fill=moon_color, outline="")
        
        self.canvas.create_rectangle(50, 140, 120, 260, fill="#0D0A22", outline="")
        self.canvas.create_rectangle(130, 110, 220, 260, fill="#0A0118", outline="")
        self.canvas.create_rectangle(230, 150, 310, 260, fill="#252A52", outline="")
        self.canvas.create_rectangle(320, 120, 420, 260, fill="#0A0118", outline="")
        
        self.canvas.create_rectangle(0, 0, 640, 260, outline="#252A52", width=6)
        
        self.canvas.create_text(480, 210, text="NEO-CAT", fill="#A9BCD6", font=("Courier New", 14, "bold"))
        self.canvas.create_text(480, 230, text="AMSTERDAM '92", fill="#A9BCD6", font=("Courier New", 12, "bold"))
        self.canvas.create_text(480, 250, text="▶ START", fill="#15E0ED", font=("Courier New", 10, "bold"))

        self.canvas.create_rectangle(20, 180, 220, 260, fill="#1B1647", outline="#2F3668", width=2)
        self.canvas.create_rectangle(30, 120, 110, 175, fill="#0A0118", outline="#2F3668")
        self.canvas.create_text(70, 140, text="AMSTERDAM 22:30", fill="#15E0ED", font=("Courier New", 6))
        
        self.canvas.create_oval(70, 190, 130, 245, fill="#2A3060", outline="#3A4275")
        self.canvas.create_rectangle(90, 160, 135, 205, fill="#2A3060", outline="#3A4275")
        self.canvas.create_polygon(90, 160, 100, 145, 110, 160, fill="#2A3060")
        self.canvas.create_polygon(115, 160, 125, 145, 135, 160, fill="#2A3060")
        self.canvas.create_rectangle(98, 175, 106, 183, fill="#15E0ED", outline="")
        self.canvas.create_rectangle(118, 175, 126, 183, fill="#15E0ED", outline="")

    def animate_scene(self):
        self.frame_count += 1
        night = (self.frame_count // 100) % 2 == 0
        
        if self.frame_count % 100 == 0:
            self.draw_scenery(night_mode=night)
            
        for drop in self.raindrops:
            drop[0] -= 2
            drop[1] += 8
            if drop[1] > 260 or drop[0] < 0:
                drop[0] = random.randint(200, 640)
                drop[1] = random.randint(0, 50)
            self.canvas.create_line(drop[0], drop[1], drop[0] - 2, drop[1] + 6, fill="#00D3F2", width=1)
            
        self.root.after(50, self.animate_scene)

    def append_chat(self, sender, message):
        self.chat_area.config(state=tk.NORMAL)
        timestamp = time.strftime('%H:%M:%S')
        self.chat_area.insert(tk.END, f"[{timestamp}] {sender}: {message}\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        
        self.append_chat("Tu", msg)
        self.msg_entry.delete(0, tk.END)
        
        state = self.cortex.reflect(cpu_load=0.22, net_latency=5)
        
        if "github" in msg.lower():
            reply = "Modulo GitHub attivo. Pronto a creare repository, gestire commit e pushare codice in autonomia."
        elif "sublime" in msg.lower():
            reply = "Lancio Sublime Text per la programmazione attiva sul tuo workspace."
            os.system("subl &")
        elif "meteo" in msg.lower():
            reply = "Oltrepò Pavese / Amsterdam '92: Condizioni dinamiche, pioggia simulata attiva nel connettoma."
        else:
            reply = f"Comando elaborato nel cortex 16-bit: '{msg}'. Stato del sistema stabile e verificato."
            
        self.append_chat("Z-KALI", reply)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ZKaliMegaDriveApp()
    app.run()
