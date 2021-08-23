#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''
import logging
import imp
import six
import importlib
from dragonfly import get_engine, get_current_engine
from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib import printer
from castervoice.lib.ctrl.configure_engine import EngineConfigEarly, EngineConfigLate
from castervoice.lib.ctrl.dependencies import DependencyMan
from castervoice.lib.ctrl.updatecheck import UpdateChecker
from castervoice.asynch import hud_support

if six.PY2:
    logging.basicConfig()

printer.out("@ - Starting {} with `{}` Engine -\n".format(settings.SOFTWARE_NAME, get_engine().name))

DependencyMan().initialize()  # requires nothing
settings.initialize()
UpdateChecker().initialize()  # requires settings/dependencies
EngineConfigEarly() # requires settings/dependencies


if control.nexus() is None:
    from castervoice.lib.ctrl.mgr.loading.load.content_loader import ContentLoader
    from castervoice.lib.ctrl.mgr.loading.load.content_request_generator import ContentRequestGenerator
    from castervoice.lib.ctrl.mgr.loading.load.reload_fn_provider import ReloadFunctionProvider
    from castervoice.lib.ctrl.mgr.loading.load.modules_access import SysModulesAccessor
    _crg = ContentRequestGenerator()
    _rp = ReloadFunctionProvider()
    _sma = SysModulesAccessor()
    _content_loader = ContentLoader(_crg, importlib.import_module, _rp.get_reload_fn(), _sma)
    control.init_nexus(_content_loader)
    EngineConfigLate() # Requires grammars to be loaded and nexus

if settings.SETTINGS["sikuli"]["enabled"]:
    from castervoice.asynch.sikuli import sikuli_controller
    sikuli_controller.get_instance().bootstrap_start_server_proxy()

try:
    imp.find_module('PySide2') # remove imp dropping python 2
    if get_current_engine().name != "text":
        hud_support.start_hud()
except ImportError:
    pass  # HUD is not available

dh = printer.get_delegating_handler()
simple_handler = printer.SimplePrintMessageHandler()
hud_ready = False
hud_message_handler = None
try:
    hud_message_handler = hud_support.HudPrintMessageHandler()
    dh.register_handler(hud_message_handler)
    printer.out("\n") # Force update to display text
    hud_ready = True
except Exception as e:
    if hud_message_handler:
        dh.unregister_handler(hud_message_handler)
    dh.register_handler(simple_handler)
    printer.out("\n") # Force update to display text
    printer.out("Hud not available.  Fell back to simple message handler.{}".format(e))

hud_ready_timeout = 10
if not hud_ready:
    import time
    time_start = time.time()
    printer.out("Waiting {} seconds for hud to start.".format(hud_ready_timeout))
    while not hud_ready and time.time() < time_start + hud_ready_timeout:
        try:
            hud_message_handler = hud_support.HudPrintMessageHandler()
            dh.register_handler(hud_message_handler)
            dh.unregister_handler(simple_handler)
            printer.out("\n") # Force update to display text
            hud_ready = True
        except Exception:
            pass
    if not hud_ready:
        printer.out("Timed out waiting for hud to start.")
