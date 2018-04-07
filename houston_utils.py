#houston_utils.py
# contains some extraneous things that we don't want cluttering up our main file

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import time
import os


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SatTest():
    def __init__(self, tx_queue):
        self.new = [] # commands that have not yet been sent out to the OBC
        self.pending = [] # commands waiting on valid response or timeout
        self.acknowledged = [] # commands that have been acknowledged properly
        self.errored = [] # commands that timed out
        self.tx_queue = tx_queue # handle for the serial transmit queue
        self.epoch = time.time
        self.raw_data = [] # raw stuff coming in from the sat

    def zero_epoch(self):
        self.utc_at_0 = time.time

    def sat_epoch(self):
        return time.time - self.utc_at_0

    def sat_epoch_at_utc(self, utc):
        return utc - self.utc_at_0 

    def add_schedule(self, data_in):
        # add a list of command dicts
        self.new = data_in

    def uplink(self, cmdid, dt):
        print("CMDID_in", str(cmdid))
        for i, dic in enumerate(self.new):
            if dic['cmdid'] == cmdid:
                break
        command = self.new[i]
        
        # rm from new list, put on pending list
        del self.new[i]
        self.pending.append(command)
        print("NEW:", self.new)
        print("command: ", command, str(i))
        print("SCHEDULED COMMAND SEND: " + str(command['cmd']))
        self.tx_queue.put(str(command['cmd']))
        return

    def process_telem(self, telem):
        receive_time = self.sat_epoch()

        # telemetry comes back as several things:
        #   - orphan messages from testing
        #   - standard telem sets
        #   - responses to immediate commands
        #   - responses to scheduled commands are stored and can be requested, since we won't always be in contact 


        # Standard telem:
        # - parse telem packet and update views. This is things like epoch, battery state, etc.
        # - every time we get one, update the HUD. Have each set available as an expandable row in a list for examination
        # - if standard telem said there were errors in the queue, we would issue a command to retrieve them 
        # - for real mission: if there were errors, automatically request them 

        # Responses to command:
        # - search pending list for any commands with timeout >= receive time
        # - sort that by ID 
        # - search that list of commands for expected response matching this one
        # - if multiple matches, go with lowest ID. put the matched command on the acknowledged list

        # Command handling on sat: 
        # - if it's an immediate command, send out the response on radio/uart right away (this is for mission and testing)
        # - if it's a sat-scheduled command, log the response so we can pull it down later 
        # - if you want to do something like read a file, you could schedule a read command of that file at the time of next downlink

        # Ottawa test:
        # put in/out of different modes, observe that the telem is reflecting that
        #       - ex: safe mode, a bunch of tasks should be suspended. we can check that from a get tasks command
        #       - ex: low power mode, check that current has dropped
        #       - these things could be different modules that we load up to create a full test, then we run the whole thing
        # schedule commands for the future (such as a chime pass), verify that they execute
        # check that telem is nominal




    def command_timeout(self, cmdid):
        pass
        # this will be called at the timeout time for a command by kivy clock
        # search the pending list for the command ID
        #   - if not there, no worries we've processed the command before timeout
        #   - if there, pull off and add to failed command list

    


