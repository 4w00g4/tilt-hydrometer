#!/usr/bin/python
import time
import blescan
import argparse
import bluetooth._bluetooth as bluez

class Tilt:
    def __init__(self, uuid, colour, temp, gravity):
        self.uuid = uuid
        self.colour = colour
        self.temp = temp
        self.gravity = gravity

    def __str__ (self, celcius=True):
        return "UUID: {u} Colour: {c} Temp: {t} Gravity {g}".format(u=self.uuid,
                                                                    c=self.colour,
                                                                    t=(celcius and ((float(self.temp) - 32) * 5/9) or self.temp),
                                                                    g=float(self.gravity)/1000)

def get_tilt(colour):
    dev_id = 0
    try:
        sock = bluez.hci_open_dev(dev_id)
        #print "ble thread started"

    except:
        print "error accessing bluetooth device..."
        return False

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)

    tilts = {
        'a495bb10c5b14b44b5121370f02d74de': 'Red',
        'a495bb20c5b14b44b5121370f02d74de': 'Green',
        'a495bb30c5b14b44b5121370f02d74de': 'Black',
        'a495bb40c5b14b44b5121370f02d74de': 'Purple',
        'a495bb50c5b14b44b5121370f02d74de': 'Orange',
        'a495bb60c5b14b44b5121370f02d74de': 'Blue',
        'a495bb70c5b14b44b5121370f02d74de': 'Pink'
    }
    all_tilts = {}

    returnedList = blescan.parse_events(sock, 100)
    for beacon in returnedList:
        if (beacon['uuid'] in tilts):
            this_tilt = Tilt(beacon['uuid'],
                                tilts[beacon['uuid']],
                                beacon['major'],
                                beacon['minor'])
            if this_tilt.colour.lower() == colour.lower():
                return this_tilt
            else:
                all_tilts[this_tilt.colour] = this_tilt

    return all_tilts

def main(args):
    colour = args.colour
    tilt = get_tilt(colour)
    if not tilt:
        print "Could not find a tilt of colour {c}".format(c=colour)
    if isinstance(tilt, list):
        print "Found these though: {o}".format(",".join(tilt.keys()))
    if isinstance(tilt, Tilt):
        print(str(tilt))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get output from a Tilt Hydrometer")
    parser.add_argument("colour", help="Colour of the tilt you want to check", type=str)
    args=parser.parse_args()

    main(args)
