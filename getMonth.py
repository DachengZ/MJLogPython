import os
import re
os.chdir(os.path.expanduser('~/Documents/MJLogPython/'))
from printHaipai import PaifuParseTool
from meld import Meld
def getMonth(month):
    folder = os.path.expanduser('~/Documents/MJLogPython/log/{}/'.format(month))
    
    if not os.path.exists(folder):
        os.mkdir(folder)
    
    if month > '200801':
        ykmlist = os.path.expanduser('~/Documents/MJLogPython/ykmjs/New/{}.txt'.format(month))
    else:
        #ykmlist = os.path.expanduser('~/Documents/MJLogPython/ykmjs/New/{}.txt'.format(month))
        raise ValueError("{} yakuman list is in an old format".format(month))
    if not os.path.isfile(ykmlist):
        raise ValueError("{} yakuman list was not prepared.".format(month))
    
    CharHaiDisp = ["<1m>", "<2m>", "<3m>", "<4m>", "<5m>", "<6m>", "<7m>", "<8m>", "<9m>", 
                   "<1p>", "<2p>", "<3p>", "<4p>", "<5p>", "<6p>", "<7p>", "<8p>", "<9p>", 
                   "<1s>", "<2s>", "<3s>", "<4s>", "<5s>", "<6s>", "<7s>", "<8s>", "<9s>", 
                   "<東>", "<南>", "<西>", "<北>", "<白>", "<發>", "<中>"]
    #cnt, cnt1 = 0, 0
    with open(ykmlist, 'rb') as file_:
        next(file_)
        next(file_)
        #                        ' time ','  name  ','[table,[   hand   ],[chiiponkon],last]' ,[yakuman(s)],'link info'
        ykmline = re.finditer(r'\'.{11}\',\'[^\']+\',\'\[\d+,\[([\d,]+)\],\[([\d,]*)\],\d+\]\',\[([\d,]*)\],\'([^\']+)\'', next(file_).decode('utf-8'))
        for ykm in ykmline:
            #cnt += 1
            hand, furu, ykmstr, info = ykm.groups()
            # print(ykm.groups())
            try:
                ykmtypes = {int(_) for _ in ykmstr.split(',')}
            except:
                # 数え役満
                s = ''.join(CharHaiDisp[int(tile) >> 2] for tile in hand.split(','))
                if len(furu) > 0:
                    s += ', ' + ', '.join(Meld(_).getInfo() for _ in furu.split(','))
                print(info)
                print(s)
            #if (37 in ykmtypes) or (38 in ykmtypes): # 天和，地和
            #    #cnt1 += 1
            #    a = PaifuParseTool(info)
            #    a.printHaiPai()
    
    #print(cnt, cnt1)
    return None

if __name__ == "__main__":
    for yr in ['2017', '2018']:
        for mn in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            getMonth(yr + mn)
