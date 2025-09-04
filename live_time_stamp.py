import asyncio
from bleak import BleakScanner, BleakClient
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

# === GESTIONE DATI PER IL GRAFICO ===
timestamps = []
temperatures = []

def handle_temperature(sender, data):
    print(f"📥 Dati grezzi da {sender}: {data.hex()} ({len(data)} byte)")

    # ⚠️ ADATTA QUESTO PARSING in base al formato dei tuoi dati!
    try:
        # Esempio: 2 byte little endian -> 0x0bfa = 3066 -> 30.66 °C
        temp_celsius = int.from_bytes(data[0:2], byteorder='little') / 100
    except Exception as e:
        print("Errore nel parsing:", e)
        return

    print(f"🌡️ Temperatura: {temp_celsius} °C")

    timestamps.append(datetime.now())
    temperatures.append(temp_celsius)

    # Mantieni gli ultimi 100 valori
    if len(timestamps) > 100:
        timestamps.pop(0)
        temperatures.pop(0)

# === GRAFICO LIVE ===
def animate(i):
    ax.clear()
    ax.plot(timestamps, temperatures, color='red')
    ax.set_title("Temperatura Live")
    ax.set_ylabel("°C")
    ax.set_xlabel("Ora")
    plt.xticks(rotation=45)
    plt.tight_layout()

# === FUNZIONE PRINCIPALE ===
async def main():
    print("🔍 Scansione dispositivi BLE...")
    devices = await BleakScanner.discover(timeout=5)
    devices = [d for d in devices if d.name is not None or d.metadata.get("manufacturer_data") or d.metadata.get("service_data")]

    if not devices:
        print("❌ Nessun dispositivo trovato.")
        return

    print("\n📡 Dispositivi trovati:")
    for i, d in enumerate(devices):
        print(f"[{i}] {d.name} ({d.address})")

    # Scegli il dispositivo
    idx = int(input("\n👉 Inserisci l'indice del dispositivo da connettere: "))
    device = devices[idx]

    print(f"\n🔗 Connessione a {device.name} ({device.address})...")
    async with BleakClient(device.address) as client:

        print("✅ Connesso!")

        # Mostra tutti i servizi/char
        notify_char = None
        print("\n🧩 Servizi e caratteristiche:")
        for service in client.services:
            print(f"[SERVICE] {service.uuid}")
            for char in service.characteristics:
                print(f"  └─ [CHAR] {char.uuid} — proprietà: {char.properties}")
                if "notify" in char.properties:
                    print("     ⚡ Possibile caratteristica temperatura!")
                    notify_char = char.uuid

        if not notify_char:
            print("❌ Nessuna caratteristica con notify trovata.")
            return

        print(f"\n📡 Avvio monitoraggio su: {notify_char}")
        await client.start_notify(notify_char, handle_temperature)

        # Avvia il grafico live
        fig, ax = plt.subplots()
        ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.show()

        await client.stop_notify(notify_char)

asyncio.run(main())
