import maya.cmds as mc
import sys
import os
sys.path.append('/usr/lib64/python2.7/site-packages')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import re

import maya.OpenMayaUI as apiUI
import sip

from guihelper import utils
reload(utils)
# from .. import utils

DEBUG=1

import logging
_logger = logging.getLogger(__name__)
_logger.propagate = DEBUG


GUIHELPER = 1

# 2015
CONTROLS = ['attrColorSliderGrp', 'attrFieldGrp', 'attrFieldSliderGrp', 'attrNavigationControlGrp', 'button', 'canvas', 'channelBox', 'checkBox', 'checkBoxGrp', 'cmdScrollFieldExecuter', 'cmdScrollFieldReporter', 'cmdShell', 'colorIndexSliderGrp', 'colorSliderButtonGrp', 'colorSliderGrp', 'commandLine', 'componentBox', 'floatField', 'floatFieldGrp', 'floatScrollBar', 'floatSlider', 'floatSlider2', 'floatSliderButtonGrp', 'floatSliderGrp', 'gradientControl', 'gradientControlNoAttr', 'helpLine', 'hudButton', 'hudSlider', 'hudSliderButton', 'iconTextButton', 'iconTextCheckBox', 'iconTextRadioButton',
            'iconTextRadioCollection', 'iconTextScrollList', 'iconTextStaticLabel', 'image', 'intField', 'intFieldGrp', 'intScrollBar', 'intSlider', 'intSliderGrp', 'layerButton', 'messageLine', 'nameField', 'nodeTreeLister', 'palettePort', 'picture', 'progressBar', 'radioButton', 'radioButtonGrp', 'radioCollection', 'rangeControl', 'scriptTable', 'scrollField', 'separator', 'shelfButton', 'soundControl', 'swatchDisplayPort', 'switchTable', 'symbolButton', 'symbolCheckBox', 'text', 'textField', 'textFieldButtonGrp', 'textFieldGrp', 'textScrollList', 'timeControl', 'timePort', 'toolButton', 'toolCollection', 'treeLister', 'treeView']

LAYOUTS = ['columnLayout', 'dockControl', 'flowLayout', 'formLayout', 'frameLayout', 'gridLayout', 'menuBarLayout',
           'paneLayout', 'rowColumnLayout', 'rowLayout', 'scrollLayout', 'shelfLayout', 'shelfTabLayout', 'tabLayout', 'toolBar']

MENUS = ['artBuildPaintMenu', 'attrEnumOptionMenu', 'attrEnumOptionMenuGrp', 'attributeMenu', 'hotBox', 'menu', 'menuEditor',
         'menuItem', 'menuSet', 'menuSetPref', 'optionMenu', 'optionMenuGrp', 'popupMenu', 'radioMenuItemCollection', 'saveMenu']


def gui_helper(path, menu=False):
    global GUIHELPER
    if GUIHELPER:
        try:
            _do_gui_helper(path, menu)
        except Exception as e:
            print 'some error', e


def _do_gui_helper(path, menu=False):
    if menu:
        mc.menuItem(l='guiHelper', subMenu=1)
    else:
        # check if menu exists already
        # _logger.info('checking if menu exists: %s|guiHelperMenu' % path )
        # if mc.menu('%s|guiHelperMenu' % path, q=1, ex=1) or mc.menu('%s||guiHelperMenu' % path, q=1, ex=1):
        #     _logger.info('menu exists skipped')
        #     return
        # else:
        mc.popupMenu('guiHelperMenu', p=path)

    build_menu(path)
    mc.setParent(menu=1)


def get_control_type(control):

    control_type = None

    for l in CONTROLS:
        # print 'checking',l
        # print 'mc.%s("%s",q=1,ex=1)' % (l, control)
        # some controls such as hudButton doesn't have -exists flag
        try:
            if eval('mc.%s("%s",q=1,ex=1)' % (l, control)) is True:
                control_type = l
                # print 'found!'
                break
        except:
            pass

    if not control_type:
        for l in LAYOUTS:
            # print 'checking',l
            if eval('mc.%s("%s",q=1,ex=1)' % (l, control)) is True:
                control_type = l
                # print 'found!'
                break

    if not control_type:
        for l in MENUS:
            # print 'checking',l
            if eval('mc.%s("%s",q=1,ex=1)' % (l, control)) is True:
                control_type = l
                # print 'found!'
                break

    return control_type


def print_flags(control):
    print 'in flags', control
    control_type = get_control_type(control)
    help = mc.help(control_type)

    print help
    print '=' * 20
    arg_help = ''

    print help.strip().split('\n')
    print '-' * 20

    for a in help.strip().split('\n')[4:-3]:

        # print 'checking',a

        flag = a.split()
        # if not flag:
        # continue

        print '  checking', flag
        if flag[1] not in ('-defineTemplate', '-parent', '-docTag', '-exists'):
            # flag_name = ' '*5+ flag[1]
            flag_name = ' ' * 5 + flag[1].ljust(25, '.')

            flag_query = eval('mc.%s("%s",%s=1,q=1)' %
                              (control_type, control, flag[1][1:]))
            if flag[1] in ('-popupMenuArray', '-childArray'):
                # flag_query = eval('mc.%s("%s",q=1)' % (control_type, flag[1]))
                if flag_query:
                    arg_help += flag_name + ' '.join(flag_query[:6]) + '\n'

            elif flag[1] == '-backgroundColor':
                # flag_query = eval('mc.%s("%s",q=1)' % (control_type, flag[1]))
                if flag_query:
                    arg_help += flag_name + str(flag_query) + '\n'
            else:
                # print 'yeah','mc.%s("%s",%s=1,q=1)' % (control_type,control, flag[1][1:])
                # flag_query = eval('mc.%s("%s",%s=1,q=1)' % (control_type,control, flag[1][1:]))
                print 'checking', flag[1][1:], '--->', flag_query

                # if flag_query is None or len(flag_query):
                arg_help += flag_name + str(flag_query) + '\n'

    print arg_help


def print_path(path):
    print '\n', '_' * 50, '\n\n'
    path_arrray = path.split('|')
    for p in path_arrray:
        print p

    print '\n', path, '\n'


def build_menu(path):
    # print 'in build_menu run !'
    ui_name = path.split('|')[-1]
    mc.menuItem(l=ui_name, c=lambda *x: sys.stdout.write(ui_name))
    mc.menuItem(d=1)
    mc.menuItem(l='Flags', c=lambda *x: print_flags(path))
    mc.menuItem(l='Print Path', c=lambda *x: print_path(path))
    mc.menuItem(d=1)
    mc.menuItem(l='guiList', c=lambda *x: print_path(path))
    mc.menuItem(l='Reveal in guiList', c=lambda *x: print_path(path))
    mc.menuItem(d=1)
    mc.menuItem(l='Parent', c=lambda *x: print_path(path))
    mc.menuItem(l='children', c=lambda *x: print_path(path))
    mc.menuItem(l='Siblings', c=lambda *x: print_path(path))
    mc.menuItem(d=1)
    mc.menuItem(l='Delete Menu', c=lambda *x: print_path(path))

    mc.menuItem(l='Help', c=lambda *x: print_path(path))


def get_window_controls(window):
    all_controls = mc.lsUI(long=1, controls=1)
    win_controls = []
    for c in all_controls:
        if '%s|' % window in c:
            win_controls.append(c)
    print win_controls

    return win_controls


def add_menu_to_all(window='all'):
    if window != 'all':
        controls = get_window_controls(window)
    else:
        controls = mc.lsUI(long=1, controls=1)

    _logger.info('in add_menu_to_all')

    # should check if menu exists before adding menus
    # or one could end up adding menu two times, and the full path becomes xxx||guiHelperMenu
    all_controls_with_menu =  get_all_control_with_menu()

    all_controls= [ re.search('^.*[^\|](?=\|)',c).group() for c in all_controls_with_menu] 
    add_count=0
    for c in controls:
        # _logger.info('add menu to: %s' % c)

        # check if menu exists already
        # it may still add redundant menus, because of ||
        # but we will take care of them in the remove function
        # _logger.info('checking if menu exists: %s|guiHelperMenu' % c )

        if c in all_controls:
        # if mc.menu('%s|guiHelperMenu' % c, q=1, ex=1):
            # _logger.info('menu exists skipped')
            continue
        else:
            gui_helper(c)
            add_count+=1

    print '\nAdded ', add_count, ' menus to ', window


def get_all_control_with_menu():
    all_menu =mc.lsUI(l=1,type='menu') or []
    controls=[]
    for m in all_menu:
        if m.endswith('guiHelperMenu'):
            controls.append(m)

    return controls



def remove_menu_from_all(window='all'):
    'run this once does not ensure all menus are removed'
    remove_count = 0
    if window != 'all':
        controls = get_window_controls(window)

        all_controls_with_menu =  get_all_control_with_menu()

        # all_controls= [ re.search('^.*[^\|](?=\|)',c).group() for c in all_controls_with_menu]

        all_controls= [ re.sub('\|+guiHelperMenu$', '', c) for c in all_controls_with_menu]



        # remove_count = 0
        for c in controls:
            # if c.split('|')[-1]=='formLayout15':
            #     print 'we are checking that formLayout15'
            #     print c

            # sometimes the menu is named ...||guiHelperMenu
            # if mc.popupMenu('%s|guiHelperMenu' % c, q=1, ex=1):
            #     # print 'found','%s||guiHelperMenu' % c
            #     mc.deleteUI('%s|guiHelperMenu' % c, menu=1)
            #     _logger.info('remove menu from | : %s' % c)
            #     remove_count += 1
                # continue
            # elif mc.popupMenu('%s||guiHelperMenu' % c, q=1, ex=1):
            #     mc.deleteUI('%s||guiHelperMenu' % c, menu=1)
            #     remove_count+=1
            #     _logger.info('remove menu from ||: %s'%c)

            if c in all_controls:
                control_with_menu = all_controls_with_menu[all_controls.index(c)]
                mc.deleteUI(control_with_menu, menu=1)


                # _logger.info('remove menu ---- : %s' % c)
                # _logger.info('remove menu from : %s' % control_with_menu)
                remove_count+=1


    else:
        # controls = mc.lsUI(long=1, controls=1)
        menus = mc.lsUI(type='menu',l=1) or []
        # menus = list(set(menus))
        menu_delete=[]
        for m in menus:
            try:
                # slow
                if m.endswith('|guiHelperMenu'):
                # if m[-14:]=='|guiHelperMenu':
                    # mc.deleteUI(m)
                    menu_delete.append(m)
                    remove_count+=1
            except:
                pass

        print 'start delete '
        mc.deleteUI(menu_delete)

        # return

        # remove_count=len(menus)

    # print '=' * 33
    # all_controls = [c.split('|')[-1] for c in controls]
    # if 'formLayout15' in all_controls:
    #     print 'yeah in !!!'



        # else:
        #     _logger.info('skipped remove menu from : %s' % c)

    print '\nRemoved ', remove_count, ' menus from ', window


def scale_ui(controls, dpi, w=True, h=True):

    for c in controls:

        control_elements = eval('mc.lsUI(type="%s")' % c) or []

        for control in control_elements:
            try:
                width = eval('mc.%s("%s",q=1,w=1)' % (c, control))
                new_width = width * dpi
                height = eval('mc.%s("%s",q=1,h=1)' % (c, control))
                new_height = height * dpi

                if w:
                    eval('mc.%s("%s",e=1,w=%d)' % (c, control, int(new_width)))
                if h:
                    eval('mc.%s("%s",e=1,h=%d)' %
                         (c, control, int(new_height)))
            except Exception as e:
                print 'error :', c, e


def set_dpi_scale(scale=1.25, scale_controls=True, scale_layouts=True, scale_menus=True):

    maya_windows = utils.getMayaWindow()
    if not hasattr(maya_windows, 'dpi_scale'):
        setattr(maya_windows, 'dpi_scale', 1)

    # for controls in [CONTROLS,LAYOUTS,MENUS]:
    # for controls in [CONTROLS,MENUS]:
    if scale_controls:
        # dpi_controls = [c for c in CONTROLS if c not in ['cmdScrollFieldExecuter', 'cmdScrollFieldReporter'] ]
        # dpi_controls =  ['shelfButton']
        dpi_controls = [
            'shelfButton', 'iconTextButton', 'iconTextCheckBox', 'toolButton']
        for controls in [dpi_controls]:
            scale_ui(controls, scale)

    if scale_layouts:
        # dpi_controls = [c for c in LAYOUTS if c not in ['cmdScrollFieldExecuter', 'cmdScrollFieldReporter'] ]
        dpi_controls = ['tabLayout', 'flowLayout']
        for controls in [dpi_controls]:
            scale_ui(controls, scale, w=False)

    if scale_menus:
        dpi_controls = [c for c in MENUS if c not in []]
        # dpi_controls =['toolBar','shelfTabLayout']
        for controls in [dpi_controls]:
            scale_ui(controls, scale)

    setattr(maya_windows, 'dpi_scale', scale)

print '1'


# set_dpi_scale()
