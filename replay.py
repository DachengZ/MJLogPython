url = '/Users/dacheng/Documents/TenhouMJLog/log/201706/2017062919gm-0089-0000-0c6b375e&tw=1&ts=0.mjlog'
import xml.etree.ElementTree as ET
readxml = ET.parse(url)
root = readxml.getroot()
root.tag, root.attrib
for elem in readxml.iter():
    print(elem.tag, elem.attrib)

MT = readxml.find('SHUFFLE').get('seed')
elem.find('seed')

import os
os.chdir('/Users/Dacheng/Documents/MJLogPython/')
from printHaipai import PaifuParseTool
a = PaifuParseTool('2010020113gm-0089-0000-b85fd1cc&tw=3&ts=0.mjlog')
a.printHaiPai()

'mt19937ar' in sys.modules
'ET' in sys.modules
