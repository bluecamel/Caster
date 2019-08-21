import time

from dragonfly import Mouse, Function, Choice

from castervoice.asynch.mouse import grids
import win32api, win32con

from castervoice.lib import control, settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


def kill():
    control.nexus().comm.get_com("grids").kill()


def send_input(pre, color, n, action):
    s = control.nexus().comm.get_com("grids")
    s.move_mouse(int(pre), int(color), int(n))
    int_a = int(action)
    if (int_a == 0) | (int_a == 1) | (int_a == -1):
        s.kill()
        grids.wait_for_death(settings.DOUGLAS_TITLE)
        time.sleep(0.1)
    if int_a == 0:
        Mouse("left").execute()
    elif int_a == 1:
        Mouse("right").execute()


def send_input_select(pre1, color1, n1, pre2, color2, n2):
    s = control.nexus().comm.get_com("grids")
    s.move_mouse(int(pre1), int(color1), int(n1))
    _x1, _y1 = win32api.GetCursorPos()
    s.move_mouse(int(pre2), int(color2), int(n2))
    _x2, _y2 = win32api.GetCursorPos()
    s.kill()
    grids.wait_for_death(settings.DOUGLAS_TITLE)
    drag_from_to(_x1,_y1,_x2,_y2)


def send_input_select_short(pre1, color1, n1, n2):
    send_input_select(pre1, color1, n1, pre1, color1, n2)


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


class RainbowGridRule(MergeRule):

    mapping = {
        "[<pre>] <color> <n> [<action>]":
            R(Function(send_input)),
        "[<pre1>] <color1> <n1> select [<pre2>] <color2> <n2>":
            R(Function(send_input_select)),
        "[<pre1>] <color1> <n1> select <n2>":
            R(Function(send_input_select_short)),
        "squat":
            R(Function(store_first_point)),
        "bench":
            R(Function(select_text)),
        SymbolSpecs.CANCEL:
            R(Function(kill)),
    }
    extras = [
        IntegerRefST("pre", 0, 9),
        IntegerRefST("pre1", 0, 9),
        IntegerRefST("pre2", 0, 9),
        Choice(
            "color", {
                "(red | rot)": 0,
                "(orange | tan | brown | braun)": 1,
                "(yellow | gelb)": 2,
                "(green | gruen)": 3,
                "(blue | blau)": 4,
                "(purple | lila)": 5
            }),
        Choice(
            "color1", {
                "(red | rot)": 0,
                "(orange | tan | brown | braun)": 1,
                "(yellow | gelb)": 2,
                "(green | gruen)": 3,
                "(blue | blau)": 4,
                "(purple | lila)": 5
            }),
        Choice(
            "color2", {
                "(red | rot)": 0,
                "(orange | tan | brown | braun)": 1,
                "(yellow | gelb)": 2,
                "(green | gruen)": 3,
                "(blue | blau)": 4,
                "(purple | lila)": 5
            }),
        IntegerRefST("n", 0, 100),
        IntegerRefST("n1", 0, 100),
        IntegerRefST("n2", 0, 100),
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
        "pre": 0,
        "pre1": 0,
        "pre2": 0,
        "action": -1,
    }


def get_rule():
    return RainbowGridRule, RuleDetails(title="rainbowgrid")
