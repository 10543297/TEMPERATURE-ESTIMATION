import asyncio
from bleak import BleakScanner

TARGET_UID = "05cb993f100000"  # tutto minuscolo per confronto

async def scan_for_uid():
    print("🔍 Scansione BLE in corso...\n")
    devices = await BleakScanner.discover(return_adv=True)

    for address, (device, adv_data) in devices.items():
        found = False
        for company_id, data in adv_data.manufacturer_data.items():
            data_hex = data.hex()
            if TARGET_UID in data_hex:
                found = True
                print(f"✅ Dispositivo trovato!")
                print(f"📡 Nome: {device.name}")
                print(f"🔗 Indirizzo: {device.address}")
                print(f"🏷  Company ID: {company_id}")
                print(f"📦 Data HEX: {data_hex}")
        if found:
            break

    if not found:
        print("❌ Nessun dispositivo trovato contenente il uid.")

asyncio.run(scan_for_uid())
