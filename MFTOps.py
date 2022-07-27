#!/bin/python3
import cmd
import os
import readline
import datetime
import importlib

import MFTCmd
import MFTMaps

histfile = '.MFTOps_history'
histfile_size = 10000
MFTCmd.logfilename="MFTOps_"+datetime.datetime.now().strftime("%Y.%m.%d_%Hh%Mm%Ss")+".log"

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
        MFTCmd.log("Starting MFTOps session. Log at " + MFTCmd.logfilename + "\n")
        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)

    def precmd(self, line):
        MFTCmd.log("=> " + datetime.datetime.now().strftime("%Y.%m.%d_%Hh%Mm%Ss") + ": " + line + "\n")
        return line

    def do_listConfigs(self, line):
        """listConfigs
        List available MFT configurations stored on MFTConfigs.py"""
        MFTCmd.listConfigs();

    def do_config(self, mode):
        """config mode
        Send MFT configuration command to FLPs. Ex: `config PHYSICS`"""
        if mode:
            MFTCmd.configMFT(mode)
        else:
            MFTCmd.log('Missing configuration mode!')
            MFTCmd.listConfigs();

    def do_customConfig(self, cfg):
        """customConfig cfg
        Send custom MFT configuration command to FLPs. ATTENTION: hx-dx is automatically appened to the end of the command line
        Ex: `./daq_init.py --gbtxload 3 --log --trig_source 4 --continuous -f 101.213 --auto_rof --scan 2 --mask 2 --name cru-`"""
        MFTCmd.customConfigMFT(cfg)

    def complete_config(self, text, line, begidx, endidx):
        text=text.upper()
        return [i for i in  MFTCmd.MFTConfigs.configMap if i.startswith(text)]

    def do_sendCommandToOncallPrompts(self, line): # Should this be moved to advanced SRC mode?
        """sendCommandToOncallPrompts command
        ADVANCED! USE WITH CARE!
        Send a command to all oncall tmux sessions"""
        for hd in MFTMaps.HalfDisks:
            MFTCmd.commandToFLPPrompt(hd, line)

    def do_enterToOncallPrompts(self, line):
        """enterToOncallPrompts
        Send ENTER to all oncall tmux sessions"""
        for hd in MFTMaps.HalfDisks:
            MFTCmd.enterToFLPPrompt(hd)

    def do_clearOncallPrompts(self, line):
        """clearOncallPrompts
        Clears all text on prompts oncall tmux sessions"""
        for hd in MFTMaps.HalfDisks:
            MFTCmd.clearFLPPrompt(hd)

    def do_interruptOncallPrompts(self, line):
        """interruptOncallPrompts
        Send interrupt request (CTRL-c) to all oncall tmux sessions`"""
        for hd in MFTMaps.HalfDisks:
            MFTCmd.interruptFLPPrompt(hd)

    def do_checkLinks(self, filter):
        """checkLinks \nReport status of all GBT links. Optional selection filter can be provided
        """
        MFTCmd.run_rocStatus(filter)

    def do_checkLinksDown(self, line):
        """checkLinksDown \nReports all GBT links which are DOWN
        """
        MFTCmd.run_rocStatus("DOWN")

    def do_checkLinksControl(self, line):
        """checkLinksControl \nReports status of control GBT links (which should be UP once MFT is moved to READY)
        """
        MFTCmd.run_rocStatus("SWT")

    def do_checkLinksControlDown(self, line):
        """checkLinksControlDown \nReports control GBT links which are down
        """
        MFTCmd.run_rocStatus("SWT.*DOWN")

    def do_errorCheck(self, line):
        """errorCheck \nList problems from last daqinit configuration
        """
        for hd in MFTMaps.HalfDisks:
            half=int(MFTCmd.getHalf(hd))
            flphost = MFTMaps.flpMap[hd]
            MFTCmd.runOnFLP(flphost, "checkMFTConfig " + hd )

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
        MFTCmd.log("Advanced mode OFF")

    __hiden_methods = ('do_EOF','do_SRC')

    def get_names(self): # To hide EOF method from help and autocompletion
        return [n for n in dir(self.__class__) if n not in self.__hiden_methods]

################################################################################
############################## ADVANCED SRC mode ###############################
################################################################################
class MFTSRC(MFTOps):
    prompt = '(MFTOps.SRC) '
    def preloop(self):
        MFTCmd.log("Advanced mode ON")
        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)

    def do_updateRUFirmware(self, command):
        """updateRUFirmware command
        ex: `updateRUFirmware  /home/mft/ru-scripts/software/py/testbench_mft.py flash_all_rdo_bitfiles /home/mft/xcku_bitfiles/v1_x_y/XCKU_vx_y_0`
        The CRU serial number is automatically passed to the firmware flash script as an enviroment variable.
        Command is sent to MFT on-call tmux sessions.
        """
        MFTCmd.log("Flash command: " + command + "\n")
        for flp in MFTMaps.MFTflps:
            for crusn in MFTMaps.cruFLPMap[flp]:
                hd = MFTMaps.cruHDMap[crusn]
                updateCmd = "CRUSN=" + crusn + " " + command
                MFTCmd.log("Sending to " + flp + " / " + hd + ": " + updateCmd)
                MFTCmd.commandToFLPPrompt(hd, updateCmd)

    def do_runOnAllFLPs(self, command):
        """runOnAllFLPs command\nRuns command on each FLP in a background session.
        On-call prompts are NOT used. Given command is executed without requesting for confirmation.
        Output is shown on MFTOps console.
        """
        for flp in MFTMaps.MFTflps:
            MFTCmd.log("Running on " + flp + ": " + command)
            MFTCmd.runOnFLP(flp,"\"" + command + "\"")

    def do_setLogLocation(self, dir):
        """setLogLocation <directory>\nSet location of log files used by errorCheck.
        This command replaces symlink ~/daq_init_logs
        """
        command = "test -d " + dir + " && { rm ~/daq_init_logs ; ln -s " + dir + " ~/daq_init_logs && echo `hostname` OK ; } || { echo ERROR: Path not found on `hostname` ; }"
        for flp in MFTMaps.MFTflps:
            MFTCmd.log("Setting log location for " + flp + ": " +dir)
            MFTCmd.runOnFLP(flp,"\"" + command + "\"")

if __name__ == '__main__':
    MFTOps().cmdloop()
