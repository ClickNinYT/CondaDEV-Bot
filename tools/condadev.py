import sys
sys.path.append('..')

from mmfparser.data.exe import ExecutableData
from mmfparser.data.gamedata import GameData
from mmfparser.data.mfa import MFA
from mmfparser.translators.pame2mfa import translate
from mmfparser.bytereader import ByteReader
from mmfparser.data.chunkloaders.imagebank import *
from mmfparser.loader import DataLoader
from misc import *

import sys
import os
import string
import os.path
import platform
                                                                                                                                                                                                                                                                                                                                                                                        
def decompile(input):
    output = os.getcwd() + '\OUTPUT'
    if input.endswith('.ccn'):
        #fp = ByteReader(open(input, 'rb'))
        #newGame = GameData(fp)
        log("Error: CCN Decompilation is not supported for now!", 0)
        exit()
    elif input.endswith('.apk'):
        #fp = ByteReader(open(input, 'rb'))
        #newGame = GameData(fp)
        log("Error: APK Decompilation is not supported for now!", 0)
        exit()
    elif input.endswith('.ipa'):
        #fp = ByteReader(open(input, 'rb'))
        #newGame = GameData(fp)
        log("Error: IPA Decompilation is not supported for now!", 0)
        exit()
    elif input.endswith('.exe'):
        fp = ByteReader(open(input, 'rb'))
        newExe = ExecutableData(fp, loadImages=True)
    else:
        log("Error: Unsupported file!", 0)
        exit()
    
    newGame = newExe.gameData

    s1 = newGame.name
    whitelist1 = string.letters + string.digits
    new_s1 = ''
    for char in s1:
        if char in whitelist1:
            new_s1 += char

    output_p = new_s1

    for file in newExe.packData.items:
        name = file.filename.split('\\')[-1]
        log('Dumping packed file %r' % name + '...', 1)
        open(os.path.join(output, name), 'wb').write(file.data)

    if newGame.files is not None:
        for file in newGame.files.items:
            name = file.name.split('\\')[-1]
            log('Dumping embedded file %r' % name + '...', 1)
            open(os.path.join(output, name), 'wb').write(str(file.data))
    newGame.files = None

    def out(value):
        log(value, 1)
    log('Translating MFA...', 1)
    newMfa = translate(newGame, print_func = out)
    s = newGame.name
    whitelist = string.letters + string.digits
    new_s = ''
    for char in s:
        if char in whitelist:
            new_s += char
    log("Application Name: " + new_s, 1)
    out_path = os.path.join(output, "output" + '.mfa')
    log('Writing MFA...', 1)
    newMfa.write(ByteReader(open(out_path, 'wb')))

    # newMfa = MFA(ByteReader(open(out_path, 'rb')))
    log('Decompilation Finished!', 1)

if __name__ == '__main__':
    inp = sys.argv[1]
    decompile(inp)
    
