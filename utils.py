# import maya.OpenMayaUI as apiUI
from PyQt4 import QtCore
import maya.OpenMayaUI as apiUI
import sip

def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)