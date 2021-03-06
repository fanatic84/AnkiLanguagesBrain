﻿#-*- coding: utf-8 -*-

#from aqt import mw, forms, ui
import datetime, os
import codecs
from languagesBrain.utils.Globals import *

logPath = os.path.join(Globals.LanguagesBrainPath, 'languagesBrain', 'log', 'main.log')

VERBOSE = False
NO_LOG = False

################################################################################
## Log / inform system
################################################################################

def debug( msg ):
    if VERBOSE: log( msg )

def log( msg ):
    if NO_LOG: return
    txt = '%s: %s' % ( datetime.datetime.now(), msg )
    f = codecs.open( logPath, 'a', 'utf-8' )
    f.write( txt + '\n' )
    f.close()
    print txt

def clearLog():
   f = codecs.open( logPath, 'w', 'utf-8' )
   f.close()