#!/bin/python3
import os
import datetime
import importlib

import MFTConfigs ## Load MFT configuration modes from MFTConfigs.py
import MFTMaps

logfilename="MFTOps.log"

def log(msg, verbose = True):
    logfile = open(logfilename, 'a')
    if verbose:
        print(msg)
    logfile.write(msg+"\n")
    logfile.close()

def getHalf(halfdisk):
    return halfdisk[1]

def checkHalfDisk(halfDisk):  # Check if halfdisk is valid
    if (halfDisk in MFTMaps.HalfDisks):
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
        flphost = MFTMaps.flpMap[halfDisk]
        cmd_prefix = "ssh -Y " + MFTMaps.flpMap[halfDisk] + "  tmux send -t oncall:0." + getHalf(halfDisk) + " HOME C-k \"\'"
        cmd_suffix = "\'\""
        os.system(cmd_prefix + command + cmd_suffix)

def runOnFLP(hostname, command): # Runs a command on the corresponding FLP
    if (hostname in MFTMaps.MFTflps):
        cmd_ = "ssh -Y " + hostname + " " + command
        os.system(cmd_ + " | tee -a " + logfilename)
    else:
        log(hostname, "is not a valid MFT FLP")

def clearFLPPrompt(halfDisk): # Clear prompt entry of the corresponding tmux terminal
    if checkHalfDisk(halfDisk):
        commandToFLPPrompt(halfDisk, "")

def enterToFLPPrompt(halfDisk): # Send ENTER to the corresponding tmux terminal
    if checkHalfDisk(halfDisk):
        flphost = MFTMaps.flpMap[halfDisk]
        cmd = "ssh -Y " + flphost + "  tmux send -t oncall:0." + getHalf(halfDisk) + " ENTER "
        os.system(cmd)

def interruptFLPPrompt(halfDisk): # Send CTRL-c to the corresponding tmux terminal
    if checkHalfDisk(halfDisk):
        flphost = MFTMaps.flpMap[halfDisk]
        cmd = "ssh -Y " + flphost + "  tmux send -t oncall:0." + getHalf(halfDisk) + " C-c "
        os.system(cmd)
def printDate():
    os.system("date +\"%d.%m.%Y %H:%M:%S %z\"" + " | tee -a " + logfilename)

def configMFT(mode): # Sends a configuration command to all MFT CRUs
    mode = mode.upper();
    if checkConfig(mode):
        for hd in MFTMaps.HalfDisks:
            configCMD = MFTConfigs.configMap[mode] + hd;
            commandToFLPPrompt(hd, configCMD)
    else:
        log(mode, "is an invalid MFT configuration.")
        listConfigs()

def customConfigMFT(cfg): # Sends a custom configuration command to all MFT CRUs; hx-dx is appened to the command
    for hd in MFTMaps.HalfDisks:
        configCMD = cfg + hd;
        commandToFLPPrompt(hd, configCMD)

def run_rocStatus(filter = ""):
    printDate()
    filter_cmd = ""
    if (filter):
        filter_cmd = " \| grep -E \"" + filter + "\""
        print_rof_status_header()
    for hd in MFTMaps.HalfDisks:
        half=int(getHalf(hd))
        flphost = MFTMaps.flpMap[hd]
        for face in range(2):
            log("\n" + hd + " face " + str(face) + " @" + flphost +  ":")
            command = "roc-status --id " + MFTMaps.CRUPCIeAdd[half][face] + filter_cmd
            runOnFLP(flphost, command)


def print_rof_status_header():
    log("================================================================================================================================================================")
    log("Link ID   GBT Mode Tx/Rx   Loopback   GBT MUX        Datapath Mode   Datapath   RX freq(MHz)   TX freq(MHz)   Status   Optical power(uW)   System ID   FEE ID ")
