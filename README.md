# 🛰️ Command Center Control Program

This project is a **Tkinter-based Command Center Control Interface**.  
It communicates through a serial (UART) connection, reads incoming data, decodes the custom protocol, and displays it in real time on the GUI.  
It simulates the communication between a **commander** and a **soldier** in an embedded system environment.

---

The system operates with a **9-byte custom data protocol** for bidirectional communication.  
Incoming data is parsed using the Python `struct` module, verified via **checksum (CSUM)**, and displayed dynamically on the GUI.  

The interface consists of two main panels:
- **Commander Panel:** Displays target coordinates, ammunition type, and command status.  
- **Soldier Panel:** Allows selection of COM port, ammunition type, and control actions such as *Fire*, *Load*, *Unload*, and *Request Permission*.

---

## 🖥️ GUI Preview

Command Center Control Interface:

<img width="564" height="425" alt="Ekran görüntüsü 2025-10-06 202125" src="https://github.com/user-attachments/assets/bc4f5c36-f636-4256-9e2b-f65605c25ed8" />


---

## 🔢 Data Packet Format

| Byte | Field Name       | Type | Description |
|------|------------------|------|-------------|
| 1    | Header           | 1B   | Fixed header byte |
| 2    | Ammunition Byte  | 1B   | Ammunition code |
| 3    | Action Byte      | 1B   | Command type |
| 4–5  | Target X         | 2B   | X coordinate |
| 6–7  | Target Y         | 2B   | Y coordinate |
| 8    | Ammo Count       | 1B   | Remaining ammunition |
| 9    | CSUM             | 1B   | Checksum (sum of previous bytes % 256) |

---

## 🧩 Technologies Used

- **Python 3.x**
- **Tkinter** — Graphical user interface
- **PySerial** — Serial communication
- **Struct** — Binary data parsing
- **Threading** — Concurrent background processing



