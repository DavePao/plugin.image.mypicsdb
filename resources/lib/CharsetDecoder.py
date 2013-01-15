#!/usr/bin/python
# -*- coding: utf8 -*-

from urllib import quote_plus
import sys, os
import xbmc


def smart_unicode(s):
    """credit : sfaxman"""
    if not s:
        return ''
    try:
        if not isinstance(s, basestring):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                s = unicode(str(s), 'UTF-8')
        elif not isinstance(s, unicode):
            s = unicode(s, 'UTF-8')
    except:
        if not isinstance(s, basestring):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                s = unicode(str(s), 'ISO-8859-1')
        elif not isinstance(s, unicode):
            s = unicode(s, 'ISO-8859-1')
    return s
    
def smart_utf8(s):
    return smart_unicode(s).encode('utf-8')
    
def get_crc32( parm ):
    parm = parm.lower()        
    byte = bytearray(parm.encode())
    crc = 0xffffffff;
    for b in byte:
        crc = crc ^ (b << 24)          
        for i in range(8):
            if (crc & 0x80000000 ):                 
                crc = (crc << 1) ^ 0x04C11DB7                
            else:
                crc = crc << 1;                        
        crc = crc & 0xFFFFFFFF
        
    return '%08x' % crc    
    
def quote_param(parm):
    parm = smart_utf8( parm.replace("\\", "\\\\\\\\").replace ("'", "\\'").replace ('"', '\\"') )
    parm = quote_plus(parm)
    
    return parm
    
def log(module, msg, level=xbmc.LOGDEBUG):
    if type(module).__name__=='unicode':
        module = module.encode('utf-8')
    
    if type(msg).__name__=='unicode':
        msg = msg.encode('utf-8')

    __filename__ = smart_utf8(os.path.basename(sys._getframe(1).f_code.co_filename))
    #'{:<30}'.format(os.path.basename(sys._getframe(1).f_code.co_filename))
    __lineno__   = str(sys._getframe(1).f_lineno)
    #'{:>6}'.format( sys._getframe(1).f_lineno)
    __addonname__    = sys.modules[ "__main__" ].__addonname__
    xbmc.log(str("[%s] line %s in %s module %s >> %s"%(__addonname__, __lineno__, __filename__, module, msg.__str__())), level)    

