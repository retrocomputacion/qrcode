###########################################
# QR Plugin for RetroBBS
###########################################
# ©2023/2025 by Durandal/Retrocomputacion
###########################################


from common.bbsdebug import _LOG,bcolors
from common.connection import Connection

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

# TML semigraphics
sgtml = [
    (' ','<RVSOFF>'),

    ('<UR-QUAD>','<RVSOFF>'),
    ('<LR-QUAD>','<RVSOFF>'),
    ('<LL-QUAD>','<RVSOFF>'),
    ('<UL-QUAD>','<RVSOFF>'),

    ('<UL-LR-QUAD>','<RVSON>'),
    ('<UL-LR-QUAD>','<RVSOFF>'),

    ('<B-HALF>','<RVSON>'),
    ('<L-HALF>','<RVSOn>'),
    ('<B-HALF>','<RVSOFF>'),
    ('<L-HALF>','<RVSOFF>'),

    ('<LR-QUAD>','<RVSON>'),
    ('<UR-QUAD>','<RVSON>'),
    ('<UL-QUAD>','<RVSON>'),
    ('<LL-QUAD>','<RVSON>'),

    (' ','<RVSON>')
]

def plugFunction(conn:Connection, data:str):

    _LOG('Rendering QR code for: '+ data, id=conn.id, v=4)

    swidth = conn.encoder.txt_geo[0]
    sheight = conn.encoder.txt_geo[1]

    qr = qrcode.QRCode(
        1,
        box_size=10,
        border=0,
    )
    qr.add_data(data)

    qrmode = qr.best_fit()
    modules = ((qrmode*4)+17)/2

    if  modules > swidth or modules > sheight:
       #String too long
        _LOG(bcolors.FAIL+'ERROR'+bcolors.ENDC+'- QRCODE: String too long',id=conn.id, v=1)
        conn.SendTML('<BR>Error! String too long')
        time.sleep(2)
        return
    offset = (((swidth-8)//2)-qrmode,((sheight-8)//2)-qrmode)

    f = io.StringIO()
    qr.make(fit=False)
    qr.print_ascii(out=f)
    f.seek(0)
    text = f.read()
    f.seek(0)
    f.close()
    qrlines = text.splitlines()
    qrout = '<BR>'*offset[1]

    for c,line in enumerate(qrlines):
        if len(line)%2 != 0:
            line = line + '\xa0'
        pairs = [line[i:i+2] for i in range(0, len(line), 2)]
        qrout += ' '*offset[0]
        rvs = '<RVSOFF>'
        for sg in pairs:
            ix = sgpairs.index(sg)
            if rvs == sgtml[ix][1]:
                qrout += sgtml[ix][0]
            else:
                qrout += sgtml[ix][1]+sgtml[ix][0]
                rvs = sgtml[ix][1]
        if c < sheight-1:
            qrout += '<BR>'
    conn.SendTML(f'<TEXT border={conn.encoder.colors["WHITE"]} background={conn.encoder.colors["WHITE"]}><CLR><BLACK>')
    conn.SendTML(qrout)
    conn.SendTML(f'<AT x=0 y={sheight-1}><RED>[<BLUE><BACK><RED>]<CURSOR enable=False>')
    conn.ReceiveKey('_')
