import asyncio
from bleak import BleakScanner

async def main():
    print("🔍 Scansione dispositivi BLE (10s)...")
    devices = await BleakScanner.discover(timeout=10)
    for d in devices:
        print(f"{d.address} - {d.name}")

asyncio.run(main())
