#!/bin/python3
import cmd
import os
import readline
import datetime
import importlib
## Load MFT configuration modes from MFTConfigs.py
import MFTConfigs

histfile = '.MFTOps_history'
histfile_size = 10000
logfilename="MFTOps_"+datetime.datetime.now().strftime("%Y.%m.%d_%Hh%Mm%Ss")+".log"
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

MFTflps = ['mftcom1', 'mftcom2', 'mftcom3', 'mftcom4', 'mftcom5']

cruMap = {"mftcom1": ["570", "567"],
    "mftcom2": ["548", "554"],
    "mftcom3": ["569", "543"],
    "mftcom4": ["552", "211"],
    "mftcom5": ["547", "542"]
}

CRUPCIeAdd=[["3b:00.0", "3c:00.0"], ["af:00.0", "b0:00.0"]]
def log(msg, verbose = True):
    logfile = open(logfilename, 'a')
    if verbose:
        print(msg)
    logfile.write(msg+"\n")
    logfile.close()

def getHalf(halfdisk):
    return halfdisk[1]

def checkHalfDisk(halfDisk):  # Check if halfdisk is valid
    if (halfDisk in HalfDisks):
        return True
    else:
        return False

def checkConfig(config):  # Check if halfdisk is valid
    importlib.reload(MFTConfigs)
    if (config in MFTConfigs.configMap):
        log(config + ": " + MFTConfigs.configMap[config] + "hx-dx\n")
        return True
    else:
        return False

def listConfigs():
    log("The following configurations are available for command 'config':\n")
    importlib.reload(MFTConfigs)
    for option in MFTConfigs.configMap:
        log(option + "\n" + MFTConfigs.configMap[option] + "hx-dx" + "\n")
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
        os.system(cmd_ + " | tee -a " + logfilename)
    else:
        log(hostname, "is not a valid MFT FLP")

def clearFLPPrompt(halfDisk): # Clear prompt entry of the corresponding tmux terminal
    if checkHalfDisk(halfDisk):
        commandToFLPPrompt(halfDisk, "")

def enterToFLPPrompt(halfDisk): # Send ENTER to the corresponding tmux terminal
    if checkHalfDisk(halfDisk):
        flphost = flpMap[halfDisk]
        cmd = "ssh -Y " + flpMap[halfDisk] + "  tmux send -t oncall:0." + getHalf(halfDisk) + " ENTER "
        os.system(cmd)

def interruptFLPPrompt(halfDisk): # Send CTRL-c to the corresponding tmux terminal
    if checkHalfDisk(halfDisk):
        flphost = flpMap[halfDisk]
        cmd = "ssh -Y " + flpMap[halfDisk] + "  tmux send -t oncall:0." + getHalf(halfDisk) + " C-c "
        os.system(cmd)
def printDate():
    os.system("date +\"%d.%m.%Y %H:%M:%S %z\"" + " | tee -a " + logfilename)

def configMFT(mode): # Sends a configuration command to all MFT CRUs
    mode = mode.upper();
    if checkConfig(mode):
        for hd in HalfDisks:
            configCMD = MFTConfigs.configMap[mode] + hd;
            commandToFLPPrompt(hd, configCMD)
    else:
        log(mode, "is an invalid MFT configuration.")
        listConfigs()

def customConfigMFT(cfg): # Sends a custom configuration command to all MFT CRUs; hx-dx is appened to the command
    for hd in HalfDisks:
        configCMD = cfg + hd;
        commandToFLPPrompt(hd, configCMD)

def run_rocStatus(filter = ""):
    printDate()
    filter_cmd = ""
    if (filter):
        filter_cmd = " \| grep -E \"" + filter + "\""
        print_rof_status_header()
    for hd in HalfDisks:
        half=int(getHalf(hd))
        flphost = flpMap[hd]
        for face in range(2):
            log("\n" + hd + " face " + str(face) + " @" + flphost +  ":")
            command = "roc-status --id " + CRUPCIeAdd[half][face] + filter_cmd
            runOnFLP(flphost, command)

def print_rof_status_header():
    log("================================================================================================================================================================")
    log("Link ID   GBT Mode Tx/Rx   Loopback   GBT MUX        Datapath Mode   Datapath   RX freq(MHz)   TX freq(MHz)   Status   Optical power(uW)   System ID   FEE ID ")

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
        log("Starting MFTOps session. Log at " + logfilename + "\n")
        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)

    def precmd(self, line):
        log("\n====> " + datetime.datetime.now().strftime("%Y.%m.%d_%Hh%Mm%Ss") + " (MFTOps) " + line, False)
        return line

    def do_listConfigs(self, line):
        """listConfigs
        List available MFT configurations stored on MFTConfigs.py"""
        listConfigs();

    def do_config(self, mode):
        """config mode
        Send MFT configuration command to FLPs. Ex: `config PHYSICS`"""
        if mode:
            configMFT(mode)
        else:
            log('Missing configuration mode!')
            listConfigs();

    def do_customConfig(self, cfg):
        """customConfig cfg
        Send custom MFT configuration command to FLPs. ATTENTION: hx-dx is automatically appened to the end of the command line
        Ex: `./daq_init.py --gbtxload 3 --log --trig_source 4 --continuous -f 101.213 --auto_rof --scan 2 --mask 2 --name cru-`"""
        customConfigMFT(cfg)

    def complete_config(self, text, line, begidx, endidx):
        text=text.upper()
        return [i for i in MFTConfigs.configMap if i.startswith(text)]

    def do_sendCommandToOncallPrompts(self, line): # Should this be moved to advanced SRC mode?
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

    def do_checkLinks(self, filter):
        """checkLinks \nReport status of all GBT links. Optional selection filter can be provided
        """
        run_rocStatus(filter)

    def do_checkLinksDown(self, line):
        """checkLinksDown \nReports all GBT links which are DOWN
        """
        run_rocStatus("DOWN")

    def do_checkLinksControl(self, line):
        """checkLinksControl \nReports status of control GBT links (which should be UP once MFT is moved to READY)
        """
        run_rocStatus("SWT")

    def do_checkLinksControlDown(self, line):
        """checkLinksControlDown \nReports control GBT links which are down
        """
        run_rocStatus("SWT.*DOWN")

    def do_errorCheck(self, line):
        """errorCheck \nList problems from last daqinit configuration
        """
        for hd in HalfDisks:
            half=int(getHalf(hd))
            flphost = flpMap[hd]
            runOnFLP(flphost, "checkMFTConfig " + hd )

    def do_exit(self, line):
        """exit
        Exit this shell. CTRL-d also works."""
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
        """SRC
        Enter advanced mode"""
        readline.set_history_length(histfile_size)
        readline.write_history_file(histfile)
        print()
        MFTSRC().cmdloop()
        log("Advanced mode OFF")

    __hiden_methods = ('do_EOF','do_SRC')

    def get_names(self): # To hide EOF method from help and autocompletion
        return [n for n in dir(self.__class__) if n not in self.__hiden_methods]

################################################################################
############################## ADVANCED SRC mode ###############################
################################################################################
class MFTSRC(MFTOps):
    prompt = '(MFTOps.SRC) '
    def preloop(self):
        log("Advanced mode ON")
        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)

    def do_updateRUFirmware(self, command):
        """updateRUFirmware command
        ex: `updateRUFirmware  /home/mft/ru-scripts/software/py/testbench_mft.py flash_all_rdo_bitfiles /home/mft/xcku_bitfiles/v1_x_y/XCKU_vx_y_0`
        The CRU serial number is automatically passed to the firmware flash script as an enviroment variable
        """
        log("\n***** WARNING ******\nYou are about to flash the firmware on all MFT ReadOut Units.\n")
        log("Flash command: " + command + "\n")
        flash = input("Are you sure?\n Type YES to continue: ")
        if flash!="YES":
            return
        for flp in MFTflps:
            for crusn in cruMap[flp]:
                updateCmd = "CRUSN=" + crusn + " " + command
                log("Running on " + flp + ": " + updateCmd)
                runOnFLP(flp,"\"" + updateCmd + "\"")

    def do_runOnAllFLPs(self, command):
        """runOnAllFLPs command\nRuns command on each FLP
        """
        for flp in MFTflps:
            log("Running on " + flp + ": " + command)
            runOnFLP(flp,"\"" + command + "\"")

if __name__ == '__main__':
    MFTOps().cmdloop()
