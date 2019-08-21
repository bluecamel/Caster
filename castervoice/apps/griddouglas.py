import time

from dragonfly import Mouse, Function, Choice

from castervoice.lib import settings, control
from castervoice.asynch.mouse import grids
import win32api, win32con

from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R

control.nexus()


def kill():
    control.nexus().comm.get_com("grids").kill()


def send_input(x, y, action):
    s = control.nexus().comm.get_com("grids")
    s.move_mouse(int(x), int(y))
    int_a = int(action)
    if (int_a == 0) | (int_a == 1) | (int_a == -1):
        s.kill()
        grids.wait_for_death(settings.DOUGLAS_TITLE)
    if int_a == 0:
        Mouse("left").execute()
    elif int_a == 1:
        Mouse("right").execute()


def send_input_select(x1, y1, x2, y2):
    s = control.nexus().comm.get_com("grids")
    s.move_mouse(int(x1), int(y1))
    _x1, _y1 = win32api.GetCursorPos()
    s.move_mouse(int(x2), int(y2))
    _x2, _y2 = win32api.GetCursorPos()
    s.kill()
    grids.wait_for_death(settings.DOUGLAS_TITLE)
    drag_from_to(_x1,_y1,_x2,_y2)


def send_input_select_short(x1, y1, x2):
    send_input_select(x1, y1, x2, y1)


def drag_from_to(x1, y1, x2, y2):
    win32api.SetCursorPos((x1,y1))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.SetCursorPos((x2,y2))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)


x1 = None
x2 = None
y1 = None
y2 = None


def store_first_point():
    global x1, y1
    x1, y1 = win32api.GetCursorPos()


def select_text():
    global x1, y1, x2, y2
    x2, y2 = win32api.GetCursorPos()
    s = control.nexus().comm.get_com("grids")
    s.kill()
    grids.wait_for_death(settings.DOUGLAS_TITLE)
    drag_from_to(x1,y1,x2,y2)


class DouglasGridRule(MergeRule):
    mapping = {
        "<x> [by] <y> [<action>]":
            R(Function(send_input)),
        "<x1> [by] <y1> (grab | select) <x2> [by] <y2>":
            R(Function(send_input_select)),
        "<x1> [by] <y1> (grab | select) <x2>":
            R(Function(send_input_select_short)),
        "squat":
            R(Function(store_first_point)),
        "bench":
            R(Function(select_text)),
        SymbolSpecs.CANCEL:
            R(Function(kill)),
    }
    extras = [
        IntegerRefST("x", 0, 300),
        IntegerRefST("y", 0, 300),
        IntegerRefST("x1", 0, 300),
        IntegerRefST("y1", 0, 300),
        IntegerRefST("x2", 0, 300),
        IntegerRefST("y2", 0, 300),
        Choice("action", {
            "kick": 0,
            "psychic": 1,
            "move": 2,
        }),
        Choice("point", {
            "one": 1,
            "two": 2,
        }),
    ]
    defaults = {
        "action": -1,
    }


def get_rule():
    return DouglasGridRule, RuleDetails(title="douglasgrid")
