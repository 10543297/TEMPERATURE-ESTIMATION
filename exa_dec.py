import asyncio
from bleak import BleakScanner, BleakClient

ADDRESS_TARGET = "8C:79:F5:1C:7E:14"  # Modifica con il MAC corretto

async def run():
    device = None

    def detection_callback(d, adv):
        nonlocal device
        if d.address == ADDRESS_TARGET:
            print(f"🔍 Dispositivo trovato: {d.address}")
            device = d

    scanner = BleakScanner(detection_callback)
    print("🔍 Scansione in corso, cercando il dispositivo target...")
    await scanner.start()

    timeout = 10
    for _ in range(timeout * 2):  # controlla per 10 secondi (loop ogni 0.5s)
        if device:
            await scanner.stop()
            break
        await asyncio.sleep(0.5)

    if not device:
        print("❌ Dispositivo target non trovato.")
        await scanner.stop()
        return

    print(f"🔗 Tentativo di connessione a {device.address}...")
    try:
        async with BleakClient(device.address) as client:
            print(f"✅ Connesso!")
            services = await client.get_services()
            for service in services:
                print(f"  📡 {service.uuid}: {service.description}")
                for char in service.characteristics:
                    print(f"    🔸 {char.uuid} ({char.properties})")
    except Exception as e:
        print(f"❌ Errore durante la connessione: {e}")

asyncio.run(run())
