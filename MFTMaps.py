#!/bin/python3

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

cruFLPMap = {"mftcom1": ["570", "567"],
    "mftcom2": ["548", "554"],
    "mftcom3": ["569", "543"],
    "mftcom4": ["552", "211"],
    "mftcom5": ["547", "542"]
}


hdCRUMap = {"h0-d0": "570",
    "h1-d4": "567",
    "h0-d1": "548",
    "h1-d3": "554",
    "h0-d2": "569",
    "h1-d2": "543",
    "h0-d3": "552",
    "h1-d1": "211",
    "h0-d4": "547",
    "h1-d0": "542"
}

cruHDMap = {"570": "h0-d0",
    "567": "h1-d4",
    "548": "h0-d1",
    "554": "h1-d3",
    "569": "h0-d2",
    "543": "h1-d2",
    "552": "h0-d3",
    "211": "h1-d1",
    "547": "h0-d4",
    "542": "h1-d0"
}

CRUPCIeAdd=[["3b:00.0", "3c:00.0"], ["af:00.0", "b0:00.0"]]
