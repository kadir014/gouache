import ctypes

import win32gui
import win32con

from src.tablet import wintab
from src.tablet.base import Tablet


def get_count() -> int:
    """ Get the number of tablet devices. """

    return wintab.get_device_count()


class Win32Tablet(Tablet):
    """
    Windows implementation for tablet input.
    """

    def __init__(self, hwnd: int, index: int = 0):
        """
        Parameters
        ----------
        @param hwnd Window handle
        @param index Tablet device index
        """
        super().__init__()

        self.device = wintab.WinTabDevice(hwnd, index)

        self._prev_wndproc = win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_WNDPROC,
            self._wndproc
        )

    def __del__(self):
        self.release()

    def release(self):
        """ Release all resources used by this tablet interface. """

        self.device.close()

    def _wndproc(self, hwnd: int, msg: int, wparam: int, lparam: int):
        if msg == 0x7ff0: # WT_DEFBASE
            self._process_packet(wparam, lparam)

        return win32gui.CallWindowProc(
            self._prev_wndproc,
            hwnd, msg, wparam, lparam
        )
        
    def _process_packet(self, wparam, lparam) -> None:
        """ Process the WinTab packet and update the pen state. """

        if lparam != self.device.context: return

        packet = wintab.PACKET()
        # WTPacket returns 0 when the packet is not found in the queue
        if not wintab.lib.WTPacket(self.device.context, wparam, ctypes.byref(packet)):
            return

        if not packet.pkChanged:
            return
        
        npres = packet.pkNormalPressure
        npres_min = self.device.pressure_min
        npres_max = self.device.pressure_max
        npres_normal = (npres + -npres_min) * (1 / float(npres_max - npres_min))
        
        self.pen.x = packet.pkX
        self.pen.y = packet.pkY
        self.pen.pressure = npres_normal
        self.pen.azimuth = packet.pkOrientation.orAzimuth / 10.0
        self.pen.tilt = packet.pkOrientation.orAltitude / 10.0