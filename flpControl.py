import cmd
import os
import readline

histfile = '.MFTOps_history'
histfile_size = 10000

HalfDisks = [
    'h0-d0', 'h1-d4', 'h0-d1', 'h1-d3', 'h0-d2', 'h1-d2', 'h0-d3', 'h1-d1',
    'h0-d4', 'h1-d0'
]

flpMap = {
    "h0-d0": "mftcom1",
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

def getHalf(halfdisk):
    return halfdisk[1]


def checkHalfDisk(halfDisk):  # Check if halfdisk is valid
    if (halfDisk in HalfDisks):
        return True
    else:
        return False


def sendFLPConfigCmd(halfDisk, mode): # Send a command to the corresponding tmux terminal
    if checkHalfDisk(halfDisk):
        flphost = flpMap[halfDisk]
        cmd_prefix="echo ssh -Y '" + flpMap[halfDisk] + " tmux send -t oncall:" + getHalf(halfDisk) + " \" echo ./config" 
        cmd_string = mode + " " + halfDisk
        cmd_suffix="\" ENTER'"
        os.system(cmd_prefix + cmd_string + cmd_suffix)


def configMFT(mode): # Sends a configuration command to all MFT CRUs
    for hd in HalfDisks:
        sendFLPConfigCmd(hd, mode)

def checkHalfDiskConfig(hd, verboseDebug = False): # WIP
    status=True
    if status:
        print(hd, "OK (fake)")
        return True
    else:
        print(hd, "NOT OK")
        if verboseDebug:
            print("TODO: show Debug lines for WARNING, ERROR, CRITICAL")
        
        return False

def checkMFTConfigStatus():
    for hd in HalfDisks:
        checkHalfDiskConfig(hd)

class MFTOps(cmd.Cmd):

    prompt = '(MFTOps) '
    lastConfig = ""

    def preloop(self):
        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)

    def do_start(self, mode):
        """start mode
        Starts MFT configuration. Ex: `start cosmics`"""
        if mode:
            self.lastConfig = mode
            print("Starting MFT configuration for", mode)
            configMFT(mode)
        else:
            print('missing argument')

    def do_reload(self, halfDisk):
        """reload halfdisk
        Reload MFT configuration for half disk. Ex: `reload h0-d1`"""
        if self.lastConfig:
            cmd_string = self.lastConfig
            sendFLPConfigCmd(halfDisk, cmd_string)

        else:
            print("No previous configuration to reload!")

    def do_checkStatus(self, hd):
        """checkStatus hal
        Check status of last MFT configuration for each halfdisk. Ex: `checkStatus`
        Check status of last MFT configuration for a given halfdisk. Ex: `checkStatus h0-d0`"""
        if hd:
            checkHalfDiskConfig(hd)
        else:
            checkMFTConfigStatus();

    def do_exit(self, line):
        return True

    def do_EOF(self, line):
        return True

    def postloop(self):
        readline.set_history_length(histfile_size)
        readline.write_history_file(histfile)
        print()


if __name__ == '__main__':
    MFTOps().cmdloop()
