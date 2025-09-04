import asyncio
from bleak import BleakScanner
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from collections import deque

# Coda circolare per gli ultimi 100 valori
times = deque(maxlen=100)
temps = deque(maxlen=100)

# MAC target del tuo sensore
TARGET_MAC = "8C:79:F5:1C:7E:14"

def decode_temperature(data: bytes) -> float:
    if len(data) >= 2:
        temp_raw = int.from_bytes(data[0:2], byteorder="little", signed=True)
        return temp_raw / 100.0
    return None

def detection_callback(device, adv_data):
    if device.address == TARGET_MAC:
        service_data = adv_data.service_data
        for uuid, data in service_data.items():
            print(f"📦 Dati ricevuti (grezzi): {data.hex()}") 
            temp = decode_temperature(data)
            if temp is not None:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Temp: {temp:.2f}°C")
                times.append(datetime.now())
                temps.append(temp)

async def main():
    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    print("📡 Scansione in corso... (interrompi con Ctrl+C)")

    # Imposta grafico
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Temperatura (°C)", color='red')
    ax.set_ylim(30, 45)
    ax.set_title("Temperatura in tempo reale")
    ax.set_xlabel("Orario")
    ax.set_ylabel("°C")
    ax.legend()

    try:
        while True:
            await asyncio.sleep(1)
            if times and temps:
                line.set_data(range(len(temps)), temps)
                ax.set_xlim(0, len(temps))
                ax.set_xticks(range(len(times)))
                ax.set_xticklabels([t.strftime("%H:%M:%S") for t in times], rotation=45, ha='right')
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
