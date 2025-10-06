import serial
import struct
import time

# Seri port ayarları
ser = serial.Serial(
    port='COM9',  # Port adı, sisteminize göre ayarlayın
    baudrate=9600,  # Baudrate, cihazınıza göre ayarlayın
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def read_message():
    response = ser.read(9)  # 9 byte'lık mesaj okuma
    if len(response) == 9:
        header, muhimmat_byte, action_byte, hedef_x, hedef_y, muhimmat_sayisi, csum = struct.unpack('>BBHHBB', response)
        calculated_csum = sum(response[:-1]) % 256
        if csum == calculated_csum:
            return {
                'header': header,
                'muhimmat_byte': muhimmat_byte,
                'action_byte': action_byte,
                'hedef_x': hedef_x,
                'hedef_y': hedef_y,
                'muhimmat_sayisi': muhimmat_sayisi,
                'csum': csum
            }
    return None

def main():
    while True:
        message = read_message()
        if message:
            print(f"Header: 0x{message['header']:02X}")
            print(f"Muhimmat Byte: 0x{message['muhimmat_byte']:02X}")
            print(f"Action Byte: 0x{message['action_byte']:02X}")
            print(f"Hedef X: {message['hedef_x']}")
            print(f"Hedef Y: {message['hedef_y']}")
            print(f"Muhimmat Sayısı: {message['muhimmat_sayisi']}")
            print(f"CSUM: 0x{message['csum']:02X}")
        time.sleep(0.01)

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import ttk
import threading

class CommandCenterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Komuta Merkez Kontrol Programı")
        self.geometry("800x400")

        self.create_widgets()
        self.running = True

        # Veri okuma thread'i başlatma
        self.read_thread = threading.Thread(target=self.read_data_loop)
        self.read_thread.start()

    def create_widgets(self):
        # Komutan kısmı
        self.header_label = ttk.Label(self, text="Header:")
        self.header_label.grid(row=0, column=0)
        self.header_value = ttk.Label(self, text="0x00")
        self.header_value.grid(row=0, column=1)

        self.muhimmat_label = ttk.Label(self, text="Muhimmat:")
        self.muhimmat_label.grid(row=1, column=0)
        self.muhimmat_value = ttk.Label(self, text="0")
        self.muhimmat_value.grid(row=1, column=1)

        self.action_label = ttk.Label(self, text="Action:")
        self.action_label.grid(row=2, column=0)
        self.action_value = ttk.Label(self, text="0")
        self.action_value.grid(row=2, column=1)

        self.hedef_x_label = ttk.Label(self, text="Hedef X:")
        self.hedef_x_label.grid(row=3, column=0)
        self.hedef_x_value = ttk.Label(self, text="0")
        self.hedef_x_value.grid(row=3, column=1)

        self.hedef_y_label = ttk.Label(self, text="Hedef Y:")
        self.hedef_y_label.grid(row=4, column=0)
        self.hedef_y_value = ttk.Label(self, text="0")
        self.hedef_y_value.grid(row=4, column=1)

        self.muhimmat_sayisi_label = ttk.Label(self, text="Muhimmat Sayısı:")
        self.muhimmat_sayisi_label.grid(row=5, column=0)
        self.muhimmat_sayisi_value = ttk.Label(self, text="0")
        self.muhimmat_sayisi_value.grid(row=5, column=1)

        self.csum_label = ttk.Label(self, text="CSUM:")
        self.csum_label.grid(row=6, column=0)
        self.csum_value = ttk.Label(self, text="0")
        self.csum_value.grid(row=6, column=1)

    def read_data_loop(self):
        while self.running:
            data = self.read_message()
            if data:
                self.update_gui(data)
                self.create_commander_message(data)
            time.sleep(0.01)

    def read_message(self):
        response = ser.read(9)  # 9 byte'lık mesaj okuma
        if len(response) == 9:
            header, muhimmat_byte, action_byte, hedef_x, hedef_y, muhimmat_sayisi, csum = struct.unpack('>BBHHBB', response)
            calculated_csum = sum(response[:-1]) % 256
            if csum == calculated_csum:
                return {
                    'header': header,
                    'muhimmat_byte': muhimmat_byte,
                    'action_byte': action_byte,
                    'hedef_x': hedef_x,
                    'hedef_y': hedef_y,
                    'muhimmat_sayisi': muhimmat_sayisi,
                    'csum': csum
                }
        return None

    def create_commander_message(self, data):
        header = 0xAD
        muhimmat_byte = data['muhimmat_byte']
        action_byte = data['action_byte']
        hedef_x = data['hedef_x']
        hedef_y = data['hedef_y']

        # 8 bytelık mesajı oluşturma
        message = struct.pack('>BBHH', header, muhimmat_byte, action_byte, hedef_x, hedef_y)
        csum = sum(message) % 256
        message += struct.pack('B', csum)

        # Arayüzde gösterme
        self.header_value.config(text=f"0x{header:02X}")
        self.muhimmat_value.config(text=muhimmat_byte)
        self.action_value.config(text=action_byte)
        self.hedef_x_value.config(text=hedef_x)
        self.hedef_y_value.config(text=hedef_y)
        self.csum_value.config(text=csum)

    def on_closing(self):
        self.running = False
        self.read_thread.join()
        ser.close()
        self.destroy()

if __name__ == "__main__":
    app = CommandCenterApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
