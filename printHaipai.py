from base64 import b64decode
import xml.etree.ElementTree as ET
from hashlib import sha512
import os
import re
import requests
from mt19937ar import MT19937ar

class PaifuParseTool:
    
    def __init__(self, info, folder = None):
        if folder is None:
            folder = os.path.expanduser('~/Documents/MJLogPython/log/') + info[:6] + '/'
        
        info = re.sub(r'\.mjlog$', '', info)
        self._filepath = folder + info + '.mjlog'
        
        if not os.path.isfile(self._filepath):
            self._downloadPaifu(info, self._filepath)
        #        01234567890123456789012345678901234567890
        #info = '2017062919gm-0089-0000-0c6b375e&tw=1&ts=0.mjlog'
        try:
            #self._view = int(re.search(r'tw=(\d+)', info).group(1))
            self._kyoku = int(re.search(r'ts=(\d+)', info).group(1))
        except:
            #self._view = 0
            self._kyoku = 0
    
    def _downloadPaifu(self, info, filepath):
        resp = requests.get("http://tenhou.net/0/log/?" + info[:31])
        resp.raise_for_status()
        with open(filepath, 'wb') as file_:
            file_.write(resp.content)
        print("Paifu {} downloaded.".format(info))
    
    def printHaiPai(self, kyoku = None, sortstyle = 1):
        try:
            tree = ET.parse(self._filepath)
            shuffle = tree.find('SHUFFLE')
        
            if shuffle is not None:
                seed = shuffle.get('seed').split(',')
                if len(seed) == 2:
                    self._printHaiPai_v3(kyoku, sortstyle)
                else:
                    self._printHaiPai_v2(kyoku, sortstyle)
            else:
                if len(tree.findall('INIT')):
                    self._printHaiPai_v1(kyoku, sortstyle)
                else:
                    self._printHaiPai_v0(kyoku, sortstyle)
        except:
            print("Preliminary XML parsing failed.")
            return None
    
    def _printHaiPai_v0(self, kyoku = 0, sortstyle = 1):
        print("No random seed no yama :(")
    
    def _printHaiPai_v1(self, kyoku = 0, sortstyle = 1):
        tree = ET.parse(self._filepath)
        if not kyoku: kyoku = self._kyoku
        RTseed = [int(_, base = 16) for _ in tree.findall('INIT')[kyoku].get('shuffle').split(',')[1:]]
        # print("Length of RTseed array is {:d}".format(len(RTseed)))
        rng = MT19937ar()
        rng.init_by_array(RTseed)
        
        yama = [i for i in range(136)]
        for i in range(135):
            tmp_index = i + rng.genrand_int32() % (136 - i)
            yama[i], yama[tmp_index] = yama[tmp_index], yama[i]
        
        #dice0 = rng.genrand_int32() % 6
        #dice1 = rng.genrand_int32() % 6
    
        self._printHaiPaifromYama(yama, kyoku, sortstyle)

    def _printHaiPai_v2(self, kyoku = 0, sortstyle = 1):
        tree = ET.parse(self._filepath)
        RTseed = [int(_, base = 16) for _ in tree.find('SHUFFLE').get('seed').split(',')[1:]]
        assert len(RTseed) == 32
        rng = MT19937ar()
        rng.init_by_array(RTseed)
        
        #dice0, dice1 = 0, 0
        if not kyoku: kyoku = self._kyoku
        for _ in range(kyoku + 1):
            rnd = [0] * 144
            src = [0] * 288
            for i in range(288):
                src[i] = rng.genrand_int32()
            for i in range(9):
                a = sha512()
                for j in range(32 * i, 32 * (i + 1)):
                    a.update(src[j].to_bytes(4, 'little'))
                b = a.digest()
                for j in range(16):
                    rnd[16 * i + j] = int.from_bytes(b[(4 * j):(4 * (j + 1))], 'little')
            
            yama = [i for i in range(136)]
            for i in range(135):
                tmp_index = i + rnd[i] % (136 - i)
                yama[i], yama[tmp_index] = yama[tmp_index], yama[i]
        
            #dice0 = rnd[135] % 6
            #dice1 = rnd[136] % 6
    
        self._printHaiPaifromYama(yama, kyoku, sortstyle)

    def _printHaiPai_v3(self, kyoku = 0, sortstyle = 1):
        tree = ET.parse(self._filepath)
        MTseed_b64 = tree.find('SHUFFLE').get('seed').split(',')[1]
        MTseed = b64decode(MTseed_b64)
        assert len(MTseed) == 2496
        RTseed = [0] * 624
        for i in range(624):
            RTseed[i] = (MTseed[4 * i + 3] << 24) | (MTseed[4 * i + 2] << 16) | (MTseed[4 * i + 1] << 8) | (MTseed[4 * i])
        
        rng = MT19937ar()
        rng.init_by_array(RTseed)
        
        #dice0, dice1 = 0, 0
        if not kyoku: kyoku = self._kyoku
        for _ in range(kyoku + 1):
            rnd = [0] * 144
            src = [0] * 288
            for i in range(288):
                src[i] = rng.genrand_int32()
            for i in range(9):
                a = sha512()
                for j in range(32 * i, 32 * (i + 1)):
                    a.update(src[j].to_bytes(4, 'little'))
                b = a.digest()
                for j in range(16):
                    rnd[16 * i + j] = int.from_bytes(b[(4 * j):(4 * (j + 1))], 'little')
            
            yama = [i for i in range(136)]
            for i in range(135):
                tmp_index = i + rnd[i] % (136 - i)
                yama[i], yama[tmp_index] = yama[tmp_index], yama[i]
        
            #dice0 = rnd[135] % 6
            #dice1 = rnd[136] % 6
    
        self._printHaiPaifromYama(yama, kyoku, sortstyle)
    
    def _printHaiPaifromYama(self, yama, kyoku = 0, sortstyle = 1):
        UnicodeHaiDisp = ["\U0001F007", "\U0001F008", "\U0001F009", "\U0001F00A", "\U0001F00B", "\U0001F00C", "\U0001F00D", "\U0001F00E", "\U0001F00F", 
                          "\U0001F019", "\U0001F01A", "\U0001F01B", "\U0001F01C", "\U0001F01D", "\U0001F01E", "\U0001F01F", "\U0001F020", "\U0001F021", 
                          "\U0001F010", "\U0001F011", "\U0001F012", "\U0001F013", "\U0001F014", "\U0001F015", "\U0001F016", "\U0001F017", "\U0001F018", 
                          "\U0001F000", "\U0001F001", "\U0001F002", "\U0001F003", "\U0001F006", "\U0001F005", "\U0001F004"]
        CharHaiDisp = ["<1m>", "<2m>", "<3m>", "<4m>", "<5m>", "<6m>", "<7m>", "<8m>", "<9m>", 
                       "<1p>", "<2p>", "<3p>", "<4p>", "<5p>", "<6p>", "<7p>", "<8p>", "<9p>", 
                       "<1s>", "<2s>", "<3s>", "<4s>", "<5s>", "<6s>", "<7s>", "<8s>", "<9s>", 
                       "<東>", "<南>", "<西>", "<北>", "<白>", "<發>", "<中>"]
        haiPaiIndex = [[135, 134, 133, 132, 119, 118, 117, 116, 103, 102, 101, 100,  87,  83], 
                       [131, 130, 129, 128, 115, 114, 113, 112,  99,  98,  97,  96,  86,  82], 
                       [127, 126, 125, 124, 111, 110, 109, 108,  95,  94,  93,  92,  85,  81], 
                       [123, 122, 121, 120, 107, 106, 105, 104,  91,  90,  89,  88,  84,  80]]
        seatName = ['东', '南', '西', '北'] # seatName = ["\u4e1c", "\u5357", "\u897f", "\u5317"]
        # seatName at E-0, not necessarily at this round
        
        print("-------Game {:02d}-------".format(kyoku))
        print("Haipai:")
        if sortstyle == 1: # Tenhou-style tile sorting
            for seat in range(4):
                print(seatName[seat] + ': ' + ''.join([UnicodeHaiDisp[tile >> 2] for tile in sorted(yama[i] for i in haiPaiIndex[seat])]))
        #elif sortstyle == 2: # Unicode-style tile sorting
        #    for seat in range(4):
        #        print(seatName[seat] + ': ' + ''.join(sorted([UnicodeHaiDisp[yama[i] >> 2] for i in haiPaiIndex[seat]])))
        else: # No tile sorting
            for seat in range(4):
                print(seatName[seat] + ': ' + ''.join([UnicodeHaiDisp[yama[i] >> 2] for i in haiPaiIndex[seat]]))        

    