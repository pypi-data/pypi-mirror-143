import _thread
import sys
from threading import Thread

from je_auto_control.utils.exception.exception_tag import je_auto_control_critical_exit_error
from je_auto_control.utils.exception.exceptions import AutoControlException
from je_auto_control.wrapper.auto_control_keyboard import keys_table
from je_auto_control.wrapper.platform_wrapper import keyboard_check


class CriticalExit(Thread):

    def __init__(self, default_daemon: bool = True):
        super().__init__()
        self.setDaemon(default_daemon)
        self._exit_check_key = keys_table.get("f7")

    def set_critical_key(self, keycode: [int, str] = None):
        """
        :param keycode which keycode we want to check is press ?
        """
        if type(keycode) is int:
            self._exit_check_key = keycode
        else:
            self._exit_check_key = keys_table.get(keycode)

    def run(self):
        """
        listener keycode _exit_check_key
        """
        try:
            while True:
                if keyboard_check.check_key_is_press(self._exit_check_key):
                    _thread.interrupt_main()
        except Exception as error:
            print(repr(error), file=sys.stderr)

    def init_critical_exit(self):
        """
        should only use this to start critical exit
        may this function will add more
        """
        critical_thread = self
        critical_thread.start()
