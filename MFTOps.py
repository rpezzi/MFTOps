#!/bin/python3
import cmd
import os
import readline

## Load MFT configuration modes from MFTConfigs.py
from MFTConfigs import *

histfile = '.MFTOps_history'
histfile_size = 10000

HalfDisks = [
    'h0-d0', 'h1-d4', 'h0-d1', 'h1-d3', 'h0-d2', 'h1-d2', 'h0-d3', 'h1-d1',
    'h0-d4', 'h1-d0'
]

flpMap = {"h0-d0": "mftcom1",
    "h1-d4": "mftcom1",
    "h0-d1": "mftcom2",
    "h1-d3": "mftcom2",
    "h0-d2": "mftcom3",
    "h1-d2": "mftcom3",
    "h0-d3": "mftcom4",
    "h1-d1": "mftcom4",
    "h0-d4": "mftcom5",
    "h1-d0": "mftcom5"
}

MFTflps = {'mftcom1', 'mftcom2', 'mftcom3', 'mftcom4', 'mftcom5'}


def getHalf(halfdisk):
    return halfdisk[1]

def checkHalfDisk(halfDisk):  # Check if halfdisk is valid
    if (halfDisk in HalfDisks):
        return True
    else:
        return False

def checkConfig(config):  # Check if halfdisk is valid
    if (config in configMap):
        print(config + ": " + configMap[config] + "hx-dx\n")
        return True
    else:
        return False

def listConfigs():
    print("The following configurations are available for command 'config':\n")
    for option in configMap:
        print(option, "\n", configMap[option] + "hx-dx","\n")
    print("\nSource: https://alice-mft-operation.docs.cern.ch/MFT%20On-Call%20Running%20Conditions/On-Call_Running_Conditions/")

def commandToFLPPrompt(halfDisk, command): # Send a command to the corresponding tmux terminal
    if checkHalfDisk(halfDisk):
        flphost = flpMap[halfDisk]
        cmd_prefix = "ssh -Y " + flpMap[halfDisk] + "  tmux send -t oncall:0." + getHalf(halfDisk) + " HOME C-k \"\'"
        cmd_suffix = "\'\""
        os.system(cmd_prefix + command + cmd_suffix)

def runOnFLP(hostname, command): # Runs a command on the corresponding FLP
    if (hostname in MFTflps):
        cmd_ = "ssh -Y " + hostname + " " + command
        os.system(cmd_)
    else:
        print(hostname, "is not a valid MFT FLP")

def clearFLPPrompt(halfDisk): # Clear prompt entry of the corresponding tmux terminal
    if checkHalfDisk(halfDisk):
        commandToFLPPrompt(halfDisk, "")

def enterToFLPPrompt(halfDisk): # Send ENTER to the corresponding tmux terminal
    if checkHalfDisk(halfDisk):
        flphost = flpMap[halfDisk]
        cmd_prefix = "ssh -Y " + flpMap[halfDisk] + "  tmux send -t oncall:0." + getHalf(halfDisk) + " ENTER "
        os.system(cmd_prefix)

def interruptFLPPrompt(halfDisk): # Send CTRL-c to the corresponding tmux terminal
    if checkHalfDisk(halfDisk):
        flphost = flpMap[halfDisk]
        cmd_prefix = "ssh -Y " + flpMap[halfDisk] + "  tmux send -t oncall:0." + getHalf(halfDisk) + " C-c "
        os.system(cmd_prefix)

def configMFT(mode): # Sends a configuration command to all MFT CRUs
    mode = mode.upper();
    if checkConfig(mode):
        for hd in HalfDisks:
            configCMD = configMap[mode] + hd;
            commandToFLPPrompt(hd, configCMD)
    else:
        print(mode, "is an invalid MFT configuration.")
        listConfigs()

def print_rof_status_header():
    print("=================================================================================================================================================================")
    print("Link ID   GBT Mode Tx/Rx   Loopback   GBT MUX        Datapath Mode   Datapath   RX freq(MHz)   TX freq(MHz)   Status   Optical power(uW)   System ID   FEE ID ")

class MFTOps(cmd.Cmd):
    prompt = '(MFTOps) '
    def preloop(self):
        print("===================")
        print("MFT Operation Shell")
        print("===================\n")

        print("The MFT Operation Shell provides a centralized interface to operate the MFT.")
        print("The shell sends commands to the oncall tmux sessions on the MFT FLPs. Status of GBT links can be checked.\n")
        print("It is based on several weak assumptions:")
        print("   1. Tmux sessions named 'oncall' where created on all FLPs")
        print("   2. Each session is split in two windows with current working dir at '~/mft-ru-cru/software/testbench'")
        print("   3. Hosts mftcom1, mftcom2, ... are locally configured for private key auth on ~/.ssh/config\n")
        print("Useful commands:")
        print("listConfigs")
        print("config NOISE")
        print("config PHYSICS")
        print("sendCommandToOncallPrompts cd ~/mft-ru-cru/software/testbench")
        print("enterToOncallPrompts")
        print("checkLinksDown")
        print("Type 'help' to view available commands; <TAB> autocompletes")
        print("Think twice before sending any command!\n")
        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)

    def do_listConfigs(self, line):
        """listConfigs
        List available MFT configurations"""
        listConfigs();

    def do_config(self, mode):
        """config mode
        Send MFT configuration command to FLPs. Ex: `config PHYSICS`"""
        if mode:
            configMFT(mode)
        else:
            print('Missing configuration mode!')
            listConfigs();

    def complete_config(self, text, line, begidx, endidx):
        text=text.upper()
        return [i for i in configMap if i.startswith(text)]

    def do_sendCommandToOncallPrompts(self, line):
        """sendCommandToOncallPrompts command
        ADVANCED! USE WITH CARE!
        Send a command to all oncall tmux sessions"""
        for hd in HalfDisks:
            commandToFLPPrompt(hd, line)

    def do_enterToOncallPrompts(self, line):
        """enterToOncallPrompts
        Send ENTER to all oncall tmux sessions"""
        for hd in HalfDisks:
            enterToFLPPrompt(hd)

    def do_clearOncallPrompts(self, line):
        """clearOncallPrompts
        Clears all text on prompts oncall tmux sessions"""
        for hd in HalfDisks:
            clearFLPPrompt(hd)

    def do_interruptOncallPrompts(self, line):
        """interruptOncallPrompts
        Send interrupt request (CTRL-c) to all oncall tmux sessions`"""
        for hd in HalfDisks:
            interruptFLPPrompt(hd)

    def do_checkLinks(self, line):
        """checkLinks \nStatus report of all GBT links
        """
        for hd in HalfDisks:
            flphost = flpMap[hd]
            print("\n" + hd + " face 0 @" + flphost +  ":")
            command = "roc-status --i=#0"
            runOnFLP(flphost, command)
            print("\n" + hd + " face 1 @" + flphost +  ":")
            command = "roc-status --i=#1"
            runOnFLP(flphost, command)

    def do_checkLinksDown(self, line):
        """checkLinksDown \nStatus report of all GBT links which are DOWN
        """
        print_rof_status_header()
        for hd in HalfDisks:
            flphost = flpMap[hd]
            print("\n" + hd + " face 0 @" + flphost +  ":")
            command = "roc-status --i=#0" + " | grep -E \"CRU|DOWN\""
            runOnFLP(flphost, command)
            print("\n" + hd + " face 1 @" + flphost +  ":")
            flphost = flpMap[hd]
            command = "roc-status --i=#1" + " | grep -E \"CRU|DOWN\""
            runOnFLP(flphost, command)

    def do_checkLinksControl(self, line):
        """checkLinksControl \nStatus report of control GBT links
        """
        print_rof_status_header()
        for hd in HalfDisks:
            flphost = flpMap[hd]
            print("\n" + hd + " face 0 @" + flphost +  ":")
            command = "roc-status --i=#0" + " | grep -E \"0         GBT|3         GBT|6         GBT|9         GBT\""
            runOnFLP(flphost, command)
            print("\n" + hd + " face 1 @" + flphost +  ":")
            command = "roc-status --i=#1" + " | grep -E \"0         GBT|3         GBT|6         GBT|9         GBT\""
            runOnFLP(flphost, command)

    def do_exit(self, line):
        """exit
        Exit this shell"""
        return True

    def emptyline(self):
        pass

    def do_EOF(self, line):
        return True

    def postloop(self):
        readline.set_history_length(histfile_size)
        readline.write_history_file(histfile)
        print()

    def do_SRC(self, line):
        """SRCMode
        Enter advanced mode"""
        readline.set_history_length(histfile_size)
        readline.write_history_file(histfile)
        print()
        MFTSRC().cmdloop()
        print("Advanced mode OFF")

    __hiden_methods = ('do_EOF','do_SRC')

    def get_names(self): # To hide EOF method from help and autocompletion
        return [n for n in dir(self.__class__) if n not in self.__hiden_methods]

class MFTSRC(MFTOps):
    prompt = '(MFTOps.SRC) '
    def preloop(self):
        print("Advanced mode ON")
        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)

    def do_updateRUFirmware(self, firmwareVersion):
        """updateFirmware firmwareVersion
        """
        print("Someday maybe...")

if __name__ == '__main__':
    MFTOps().cmdloop()
