import asyncio
from bleak import BleakScanner
from datetime import datetime
from collections import deque
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

# === Configurazioni ===
uid_to_find = "05CB993F100000"
patchId_to_find = "cma3neyd100004h6zfj8tj8e3"
TARGET_UUID = "0000fef3-0000-1000-8000-00805f9b34fb"

# === Preparazione grafico ===
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], label="Temperatura (°C)", color='red')
ax.set_ylim(30, 45)
ax.set_title("Temperatura in tempo reale")
ax.set_xlabel("Orario")
ax.set_ylabel("°C")
ax.legend()

# === Buffer circolari ===
times = deque(maxlen=100)
temps = deque(maxlen=100)

# === Decodifica temperatura da raw data ===
def decode_temperature(data: bytes) -> float:
    if len(data) >= 2:
        temp_raw = int.from_bytes(data[0:2], byteorder="little", signed=True)
        temp_celsius = (temp_raw / 100.0) - 25  # 🔧 Calibrazione basata sui tuoi dati
        return temp_celsius
    return None

# === Callback su ogni dispositivo rilevato ===
def detection_callback(device, advertisement_data):
    # Debug opzionale: stampa ogni pacchetto
    print(f"Dispositivo: {device.address}, dati adv: {advertisement_data}")

    # Filtro su UUID dei servizi
    if TARGET_UUID in advertisement_data.service_data:
        data = advertisement_data.service_data[TARGET_UUID]
        temp = decode_temperature(data)

        if temp is not None:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Temp: {temp:.2f}°C")
            times.append(datetime.now())
            temps.append(temp)

    # Ulteriore filtro: cerca UID nei manufacturer data
    for mfg_id, mfg_data in advertisement_data.manufacturer_data.items():
        if uid_to_find.encode() in mfg_data:
            print(f"✅ UID rilevato nel manufacturer data: {mfg_data}")
        if patchId_to_find.encode() in mfg_data:
            print(f"✅ Patch ID rilevato nel manufacturer data: {mfg_data}")

# === Loop principale ===
async def main():
    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    print("🔍 Scansione in corso... (Ctrl+C per fermare)")

    try:
        while True:
            await asyncio.sleep(1)
            if times and temps:
                line.set_data(times, temps)
                ax.set_xlim(times[0], times[-1])
                ax.relim()
                ax.autoscale_view()
                plt.draw()
                plt.pause(0.01)
    except KeyboardInterrupt:
        print("🛑 Interrotto.")
    finally:
        await scanner.stop()

if __name__ == "__main__":
    asyncio.run(main())
