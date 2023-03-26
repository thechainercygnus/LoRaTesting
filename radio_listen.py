import time
import busio
from digitalio import DigitalInOut
import board
import adafruit_rfm9x


CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    print('Initializing radio')
    print(f'Initialized with station ID {rfm9x.node}')
    station_id = int(input('Enter station ID (0-255): '))
    if station_id >= 0 and station_id <= 255:
        rfm9x.node = station_id
        print(f'Setting station id to: {rfm9x.node}')
    print('Radio has been initiazlied')
    print('--------------------------')
except RuntimeError as error:
    print(f"RFM9x Error {error}")
    
prev_packet = None
while True:
    packet = None
    packet = rfm9x.receive()
    if packet is None:
        print('No messages.')
    else:
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        print(packet_text)
        time.sleep(1)
    time.sleep(0.1)