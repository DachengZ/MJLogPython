import xml.etree.ElementTree as ET
import os
os.chdir(os.path.expanduser('~/Documents/MJLogPython/'))
from printHaipai import PaifuParseTool
a = PaifuParseTool('2017073123gm-0029-0000-be75e007&tw=0&ts=7.mjlog')
#a = PaifuParseTool('2010020113gm-0089-0000-b85fd1cc&tw=3&ts=0.mjlog')
#a = PaifuParseTool('2009071817gm-00c1-0000-3a507b6f&tw=2&ts=2.mjlog')
#a = PaifuParseTool('2009070522gm-00c1-0000-a4fd12c0&tw=1&ts=0.mjlog')
a.printHaiPai()