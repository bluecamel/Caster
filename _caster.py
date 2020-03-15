#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''

import imp
import logging
import sys

from dragonfly import get_engine
from dragonfly import RecognitionObserver

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.ctrl.configure_engine import EngineConfigEarly, EngineConfigLate
from castervoice.lib.ctrl.dependencies import DependencyMan
from castervoice.lib.ctrl.updatecheck import UpdateChecker
from castervoice.lib.utilities import start_hud


_DARWIN = sys.platform == "darwin"


class LoggingHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.hud = control.nexus().comm.get_com("hud")

    def emit(self, record):
        try:
            self.hud.send("# {}".format(record.msg))
        except ConnectionRefusedError:  # pylint: disable=undefined-variable
            print("# {}".format(record.msg))


class Observer(RecognitionObserver):
    def __init__(self):
        self.hud = control.nexus().comm.get_com("hud")

    def on_begin(self):
        pass

    def on_recognition(self, words):
        try:
            self.hud.send("$ {}".format(" ".join(words)))
        except ConnectionRefusedError:  # pylint: disable=undefined-variable
            print("$ {}".format(" ".join(words)))

    def on_failure(self):
        try:
            self.hud.send("?!")
        except ConnectionRefusedError:  # pylint: disable=undefined-variable
            print("?!")


def main():
    logging.basicConfig(format="%(asctime)s :%(levelname)s:%(name)s:%(funcName)s -- %(message)s")
    DependencyMan().initialize()  # requires nothing
    settings.initialize()
    UpdateChecker().initialize()  # requires settings/dependencies
    EngineConfigEarly() # requires settings/dependencies

    if _DARWIN:
        import kaldi_active_grammar
        kaldi_active_grammar.disable_donation_message()
        engine = get_engine(
            "kaldi",
            model_dir=settings.SETTINGS["engine"]["model_dir"],
            tmp_dir=settings.SETTINGS["engine"]["tmp_dir"],
            vad_aggressiveness=settings.SETTINGS["engine"]["aggressiveness"],
            vad_padding_start_ms=settings.SETTINGS["engine"]["padding_start"],
            vad_padding_end_ms=settings.SETTINGS["engine"]["padding_end"],
            vad_complex_padding_end_ms=settings.SETTINGS["engine"]["complex_padding_end"],
            auto_add_to_user_lexicon=True)
        engine.connect()
    else:
        engine = get_engine()

    if get_engine()._name in ["sapi5shared", "sapi5", "sapi5inproc"]:
        settings.WSR = True
        from castervoice.rules.ccr.standard import SymbolSpecs
        SymbolSpecs.set_cancel_word("escape")

    if control.nexus() is None:
        from castervoice.lib.ctrl.mgr.loading.load.content_loader import ContentLoader
        from castervoice.lib.ctrl.mgr.loading.load.content_request_generator import ContentRequestGenerator
        crg = ContentRequestGenerator()
        content_loader = ContentLoader(crg)
        control.init_nexus(content_loader)
        EngineConfigLate() # Requires grammars to be loaded and nexus

    if settings.SETTINGS["sikuli"]["enabled"]:
        from castervoice.asynch.sikuli import sikuli_controller
        sikuli_controller.get_instance().bootstrap_start_server_proxy()

    print("\n*- Starting " + settings.SOFTWARE_NAME + " -*")

    try:
        imp.find_module('PySide2')
        start_hud()
        logger = logging.getLogger('caster')
        logger.addHandler(LoggingHandler())  # must be after nexus initialization
        logger.setLevel(logging.DEBUG)
        Observer().register()  # must be after HUD process has started
        engine.do_recognition()
    except ImportError:
        pass  # HUD is not available
    except KeyboardInterrupt:
        try:
            control.nexus().comm.get_com("hud").kill()
        except ConnectionRefusedError:
            pass


def TEST():
    logger = logging.getLogger('caster')
    logger.setLevel(logging.DEBUG)
    DependencyMan().initialize()
    settings.initialize()
    UpdateChecker().initialize()
    if control.nexus() is None:
        import castervoice.lib.ctrl.mgr.loading.load.content_loader as cl
        import castervoice.lib.ctrl.mgr.loading.load.content_request_generator as crg
        content_loader = cl.ContentLoader(crg.ContentRequestGenerator())
        control.init_nexus(content_loader)
    print("\n*- Testing " + settings.SOFTWARE_NAME + " -*")


if __name__ == "__main__":
    main()
else:
    TEST()
