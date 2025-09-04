from bleak import BleakScanner

uid_to_find = "05CB993F100000"
patchId_to_find = "cma3neyd100004h6zfj8tj8e3"

def detection_callback(device, advertisement_data):
    # Qui puoi stampare i dati ricevuti per capire dove cercare uid e patchId
    print(f"Dispositivo: {device}, dati adv: {advertisement_data}")
    
    # Esempio: se uid è nel nome del dispositivo
    if device.name and uid_to_find in device.name:
        print(f"Trovato dispositivo con uid: {device.name}")
    # Oppure, se i dati custom sono nel manufacturer_data
    for mfg_id, mfg_data in advertisement_data.manufacturer_data.items():
        if uid_to_find.encode() in mfg_data:
            print(f"Trovato uid nel manufacturer data: {mfg_data}")

async def main():
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(5)  # scansione per 5 secondi
    await scanner.stop()

import asyncio
asyncio.run(main())
