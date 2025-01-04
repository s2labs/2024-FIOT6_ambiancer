import asyncio
import time

from bleak import BleakClient
from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

ADDRESS = "ff:21:09:28:22:5a"
CHARACTERISTIC = "0000fff3-0000-1000-8000-00805f9b34fb"
HEADER = "BC040600"
FOOTER = "EB000055"
len_payload = 4
pld=["070398", "0A02BC", "0C039C", "0D039C", "52034A", "5D0326", "5601A4", "5801AC", "5C02DB", "08032A"]
async def main():
    device = await BleakScanner.find_device_by_address(ADDRESS, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ADDRESS} could not be found.")
    async with BleakClient(device) as client:
        svcs = await client.get_services()

        #data = "00000000"
        """for i in range(0,65536,10):
            hex_code = str(hex(i))
            payload = "0" * (len_payload - len(hex_code[2:])) + hex_code[2:]
            packet=HEADER+payload+FOOTER"""
        for i in pld:
            packet=HEADER+i+FOOTER[2:]
            #print(packet)
            await client.write_gatt_char(CHARACTERISTIC, bytearray.fromhex(packet))
            print(f"Sending {i}")
            time.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())

