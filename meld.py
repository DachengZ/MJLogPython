class Meld:
    _CharHaiDisp = ["<1m>", "<2m>", "<3m>", "<4m>", "<5m>", "<6m>", "<7m>", "<8m>", "<9m>", 
                         "<1p>", "<2p>", "<3p>", "<4p>", "<5p>", "<6p>", "<7p>", "<8p>", "<9p>", 
                         "<1s>", "<2s>", "<3s>", "<4s>", "<5s>", "<6s>", "<7s>", "<8s>", "<9s>", 
                         "<東>", "<南>", "<西>", "<北>", "<白>", "<發>", "<中>"]
    
    def __init__(self, meld):
        meld = int(meld)
        self._seatFrom = ['自己', '下家', '对家', '上家'][meld & 3]
        if (meld >> 2) & 1:
            self._meldtype = '吃'
            furu = (meld >> 10) & 63
            q, r = divmod(furu, 3)
            tile1 = (q // 7) * 9 + (q % 7)
            self._handTile = [tile1 + rr for rr in range(3) if rr != r]
            self._nakiTile = tile1 + r
            # TODO: use bit4-9 to distinguish red tiles from normal ones
        elif (meld >> 3) & 1:
            self._meldtype = '碰'
            furu = (meld >> 9) & 127;
            q, r = divmod(furu, 3)
            self._handTile = [q, q]
            self._nakiTile = q
            # TODO: use bit5-6, bit9-15 to distinguish red tiles from normal ones
        else:
            if (meld >> 4) & 1:
                self._meldtype = '加'
                furu = (meld >> 9) & 127
                q, r = divmod(furu, 3)
                self._handTile = [q, q]
                self._nakiTile = q
            # TODO
            else:
                self._meldtype = '杠'
                #self._meldtype = '明' if (meld & 3) else '暗'
                furu = (meld >> 8) & 255
                q = furu >> 2
                self._handTile = [q, q]
                self._nakiTile = q
        self._printInfo = self._CharHaiDisp[self._handTile[0]] + self._CharHaiDisp[self._handTile[1]] + self._meldtype + self._seatFrom + self._CharHaiDisp[self._nakiTile]
    
    def getInfo(self):
        return self._printInfo
    
    def __str__(self):
        print(self._printInfo)