import tkinter as tk
import threading

def highlight_area(x, y, w, h, duration=1.0):
    def show():
        root = tk.Tk()
        root.overrideredirect(True)  # sem bordas
        root.attributes("-topmost", True)
        root.attributes("-alpha", 0.4)  # transparência
        root.configure(bg='red')

        # Posição e tamanho
        root.geometry(f"{w}x{h}+{x}+{y}")

        # Fecha após 'duration' segundos
        root.after(int(duration * 1000), root.destroy)
        root.mainloop()

    # Executa em thread para não travar
    threading.Thread(target=show).start()
