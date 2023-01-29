#######################################
# QR Plugin for RetroBBS
#######################################
# ©2023 by Durandal/Retrocomputacion
#######################################


from common.bbsdebug import _LOG,bcolors
import common.helpers as H
import common.style as S
from common.connection import Connection
import common.petscii as P
import common.turbo56k as TT

import qrcode
import io
import time


#############################
#Plugin setup
def setup():
    fname = "QRCODE" #UPPERCASE function name for config.ini
    parpairs = [('text','')] #config.ini Parameter pairs (name,defaultvalue)
    return(fname,parpairs)
#############################

# Unicode semigraphic pairs
sgpairs = [
    chr(0xa0)+chr(0xa0),
    
    chr(0xa0)+chr(0x2580),
    chr(0xa0)+chr(0x2584),
    chr(0x2584)+chr(0xa0),
    chr(0x2580)+chr(0xa0),

    chr(0x2584)+chr(0x2580),
    chr(0x2580)+chr(0x2584),

    chr(0x2580)+chr(0x2580),
    chr(0xa0)+chr(0x2588),
    chr(0x2584)+chr(0x2584),
    chr(0x2588)+chr(0xa0),
    
    chr(0x2588)+chr(0x2580),
    chr(0x2588)+chr(0x2584),
    chr(0x2584)+chr(0x2588),
    chr(0x2580)+chr(0x2588),

    chr(0x2588)+chr(0x2588)
    ]

# PETSCII semigraphics (code,reverse)
sgpet = [
    (b'\x20',b'\x92'),

    (b'\xbc',b'\x92'),
    (b'\xac',b'\x92'),
    (b'\xbb',b'\x92'),
    (b'\xbe',b'\x92'),

    (b'\xbf',b'\x12'),
    (b'\xbf',b'\x92'),

    (b'\xa2',b'\x12'),
    (b'\xa1',b'\x12'),
    (b'\xa2',b'\x92'),
    (b'\xa1',b'\x92'),

    (b'\xac',b'\x12'),
    (b'\xbc',b'\x12'),
    (b'\xbe',b'\x12'),
    (b'\xbb',b'\x12'),

    (b'\x20',b'\x12')
]

def plugFunction(conn:Connection, data:str):

    _LOG('Rendering QR code for: '+ data, id=conn.id, v=4)

    qr = qrcode.QRCode(
        1,
        box_size=10,
        border=0,
    )
    qr.add_data(data)

    qrmode = qr.best_fit()

    if  qrmode > 8:
       #String too long
        _LOG(bcolors.FAIL+'ERROR'+bcolors.ENDC+'- QRCODE: String too long',id=conn.id, v=1)
        conn.Sendall(P.toPETSCII('\rError! String too long'))
        time.sleep(2)
        return
    offset = (16-qrmode,8-qrmode)

    f = io.StringIO()
    qr.make(fit=False)
    qr.print_ascii(out=f)
    f.seek(0)
    text = f.read()
    f.seek(0)
    f.close()
    qrlines = text.splitlines()
    petout = b'\r'*offset[1]

    for c,line in enumerate(qrlines):
        if len(line)%2 != 0:
            line = line + '\xa0'
        pairs = [line[i:i+2] for i in range(0, len(line), 2)]
        petout += b' '*offset[0]
        rvs = b'\x92'
        for sg in pairs:
            ix = sgpairs.index(sg)
            if rvs == sgpet[ix][1]:
                petout += sgpet[ix][0]
            else:
                petout += sgpet[ix][1]+sgpet[ix][0]
                rvs = sgpet[ix][1]
        if c < 24:
            petout += b'\r'
    conn.Sendall(TT.to_Text(0,1,1)+chr(P.CLEAR)+chr(P.BLACK))
    conn.Sendallbin(petout)
    conn.Sendall(TT.set_CRSR(0,24)+chr(P.RED)+'['+chr(P.BLUE)+'_eXIT'+chr(P.RED)+']')
    conn.ReceiveKey(b'_')
