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
    send_msg = input('Send new message [Y/n]: ')
    if send_msg != 'n':
        destination_station_id = int(input('Enter target station id (0-255): '))
        message = input(f'Enter message to send to station {destination_station_id}: ')
        msg_byte_array = bytearray()
        msg_byte_array.extend(map(ord, message))
        if destination_station_id >= 0 and destination_station_id <= 255 and destination_station_id != rfm9x.node:
            rfm9x.send(msg_byte_array, destination=destination_station_id)
except RuntimeError as error:
    print(f"RFM9x Error {error}")
