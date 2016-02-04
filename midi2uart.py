import jack
import binascii
import serial
import sys

#UART_DEVICE = '/dev/ttyUSB0'
UART_DEVICE = '/dev/ttyACM0'

UART_BAUD = 31250
#UART_BAUD = 38400


if __name__ == "__main__":


    client = jack.Client("MIDI2UART")
    _ser = serial.Serial(UART_DEVICE, UART_BAUD, timeout=50)

    port = client.midi_inports.register("input1")

    @client.set_process_callback
    def process(frames):
        for offset, data in port.incoming_midi_events():

            pkt = data

            _ser.write(pkt)

            #print("{0}: 0x{1}".format(client.last_frame_time + offset, binascii.hexlify(data).decode()))


    with client:
        print("#" * 80)
        print("press Return to quit")
        print("#" * 80)

        cnt = 0
        while True:
            cnt = cnt+1
            data = _ser.read(size=1)
            sys.stdout.write("0x%s "%binascii.hexlify(data).decode())


            # temporary parsing: new line after 5 byte (BLE: timestamp + NOTE ON/OFF)
            if cnt >= 5:
                sys.stdout.write("\n")
                cnt=0
