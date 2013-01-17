#!/usr/bin/python
# -*- coding: utf8 -*-

""" 
Common functions.
Copyright (C) 2012 Xycl

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""


import sys, os, urllib
import xbmc, xbmcaddon

__addonname__    = sys.modules[ "__main__" ].__addonname__
__settings__ = xbmcaddon.Addon(id=__addonname__)
__language__ = __settings__.getLocalizedString
__homepath__ = __settings__.getAddonInfo('path').decode('utf-8')
__sys_file_encoding__ = sys.getfilesystemencoding()

def getaddon_path():
    return __homepath__

def getaddon_name():
    __settings__.getAddonInfo('name')
    
def getaddon_info(parm):
    return __settings__.getAddonInfo(parm)


def getstring(num):
    return __language__(num)


# taken from: http://wiki.xbmc.org/index.php?title=Xbmcaddon_module
def openaddon_settings():
    __settings__.openSettings()


def getaddon_setting(name):
    return __settings__.getSetting(name)


def setaddon_setting(name, value):
    __settings__.setSetting(id=name, value=value)


# helpers
def show_notification(title, message, timeout=2000):
    command = 'Notification(%s,%s,%s)' % (smart_utf8(title), smart_utf8(message), timeout)
    xbmc.executebuiltin(command)


def run_plugin(plugin, params=""):
    if params != "":
        quoted_params = [ name+"="+quote_param(value)+"&" for (name, value) in params][:-1]
        xbmc.executebuiltin('XBMC.RunPlugin(%s?%s)'%(plugin, quoted_params))
    else:
        xbmc.executebuiltin('XBMC.RunPlugin(%s)'%plugin)


def run_script(script, args=""):
    if args == "":
        xbmc.executebuiltin('XBMC.RunScript(%s)'%script)    
    else:
        xbmc.executebuiltin('XBMC.RunScript(%s,%s)'%(script, args))    


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
    parm = urllib.quote_plus(parm)

    return parm


def unquote_param(parm):
    parm = urllib.unquote_plus(parm)
    parm = smart_utf8( parm.replace ('\\"', '"').replace ("\\'", "'").replace("\\\\\\\\", "\\") )

    return parm


def unquote_unicode(text):
    def unicode_unquoter(match):
        return unichr(int(match.group(1),16))
    return re.sub(r'&#([0-9])*?;',unicode_unquoter,text)


def log(module, msg, level=xbmc.LOGDEBUG):
    if type(module).__name__=='unicode':
        module = module.encode('utf-8')

    if type(msg).__name__=='unicode':
        msg = msg.encode('utf-8')

    filename = smart_utf8(os.path.basename(sys._getframe(1).f_code.co_filename))
    lineno  = str(sys._getframe(1).f_lineno)

    #print sys._getframe(1).f_globals
    
    if len(module.strip()) == 0:
        try:
            module = "function " + sys._getframe(1).f_code.co_name
        except:
            module = " "
            pass
    else:
        module = 'object ' + module
    xbmc.log(str("[%s] line %5d in %s %s >> %s"%(__addonname__, int(lineno), filename, module, msg.__str__())), level)    

