"""
This module wraps a subset of the WinTab SDK used by Wacom and many other
graphic tablets and programs as an interface on Windows.

Reference:
https://developer-docs.wacom.com/docs/icbt/windows/wintab/wintab-reference

Sample codes on Github:
https://github.com/Wacom-Developer/wacom-device-kit-windows
"""

import ctypes
from ctypes.wintypes import (
    HANDLE,
    HWND,
    BOOL,
    UINT,
    LONG,
    DWORD,
    WCHAR,
    LPVOID
)


FIX32 = DWORD # fixed-point arithmetic type
WTPKT = DWORD # packet mask
HCTX  = HANDLE # context handle


class PK:
    """
    WTPKT bits
    https://developer-docs.wacom.com/docs/icbt/windows/wintab/wintab-reference/#wtpkt
    """

    CONTEXT          = 0x0001 # reporting context
    STATUS           = 0x0002 # status bits
    TIME             = 0x0004 # time stamp
    CHANGED          = 0x0008 # change bit vector
    SERIAL_NUMBER    = 0x0010 # packet serial number
    CURSOR           = 0x0020 # reporting cursor
    BUTTONS          = 0x0040 # button information
    X                = 0x0080 # x axis
    Y                = 0x0100 # y axis
    Z                = 0x0200 # z axis
    NORMAL_PRESSURE  = 0x0400 # normal or tip pressure
    TANGENT_PRESSURE = 0x0800 # tangential or barrel pressure
    ORIENTATION      = 0x1000 # orientation info: tilts
    ROTATION         = 0x2000 # rotation info; 1.1


class WTI:
    """
    Information categories
    https://developer-docs.wacom.com/docs/icbt/windows/wintab/wintab-reference/#information-categories-and-indices
    """

    INTERFACE  = 1
    DEVICES    = 100
    DEFCONTEXT = 3
    DEFSYSCTX  = 4 # System context


class DVC:
    """
    https://developer-docs.wacom.com/docs/icbt/windows/wintab/wintab-reference/#wti_devices-index-definitions
    """

    NAME        = 1
    HARDWARE    = 2
    NCSRTYPES   = 3
    FIRSTCSR    = 4
    PKTRATE     = 5
    PKTDATA     = 6
    PKTMODE     = 7
    CSRDATA     = 8
    XMARGIN     = 9
    YMARGIN     = 10
    ZMARGIN     = 11
    X           = 12
    Y           = 13
    Z           = 14
    NPRESSURE   = 15
    TPRESSURE   = 16
    ORIENTATION = 17
    ROTATION    = 18 # 1.1
    PNPID       = 19 # 1.1


class IFC:
    """
    https://developer-docs.wacom.com/docs/icbt/windows/wintab/wintab-reference/#wti_interface-index-definitions
    """

    WINTABID = 1
    SPECVERSION = 2
    IMPLVERSION = 3
    NDEVICES = 4
    NCURSORS = 5
    NCONTEXTS = 6
    CTXOPTIONS = 7
    CTXSAVESIZE = 8
    NEXTENSIONS = 9
    NMANAGERS = 10


class AXIS(ctypes.Structure):
    """
    Range and Resolution Descriptor
    https://developer-docs.wacom.com/docs/icbt/windows/wintab/wintab-reference/#axis
    """

    _fields_ = (
        ("axMin", LONG),
        ("axMax", LONG),
        ("axUnits", UINT),
        ("axResolution", FIX32)
    )


class LOGCONTEXT(ctypes.Structure):
    """
    https://developer-docs.wacom.com/docs/icbt/windows/wintab/wintab-reference/#logcontext
    """

    _fields_ = (
        ("lcName", WCHAR * 40),
        ("lcOptions", UINT),
        ("lcStatus", UINT),
        ("lcLocks", UINT),
        ("lcMsgBase", UINT),
        ("lcDevice", UINT),
        ("lcPktRate", UINT),
        ("lcPktData", WTPKT),
        ("lcPktMode", WTPKT),
        ("lcMoveMask", WTPKT),
        ("lcBtnDnMask", DWORD),
        ("lcBtnUpMask", DWORD),
        ("lcInOrgX", LONG),
        ("lcInOrgY", LONG),
        ("lcInOrgZ", LONG),
        ("lcInExtX", LONG),
        ("lcInExtY", LONG),
        ("lcInExtZ", LONG),
        ("lcOutOrgX", LONG),
        ("lcOutOrgY", LONG),
        ("lcOutOrgZ", LONG),
        ("lcOutExtX", LONG),
        ("lcOutExtY", LONG),
        ("lcOutExtZ", LONG),
        ("lcSensX", FIX32),
        ("lcSensY", FIX32),
        ("lcSensZ", FIX32),
        ("lcSysMode", BOOL),
        ("lcSysOrgX", ctypes.c_int),
        ("lcSysOrgY", ctypes.c_int),
        ("lcSysExtX", ctypes.c_int),
        ("lcSysExtY", ctypes.c_int),
        ("lcSysSensX", FIX32),
        ("lcSysSensY", FIX32),
    )


class ORIENTATION(ctypes.Structure):
    """
    https://developer-docs.wacom.com/docs/icbt/windows/wintab/wintab-reference/#orientation
    """

    _fields_ = (
        ("orAzimuth", ctypes.c_int),
        ("orAltitude", ctypes.c_int),
        ("orTwist", ctypes.c_int)
    )


class PACKET(ctypes.Structure):
    _fields_ = (
        ("pkChanged", WTPKT),
        ("pkX", LONG),
        ("pkY", LONG),
        ("pkZ", LONG),
        ("pkNormalPressure", UINT),
        ("pkTangentPressure", UINT),
        ("pkOrientation", ORIENTATION),
    )


lib = ctypes.windll.wintab32

lib.WTOpenW.restype = HCTX
lib.WTOpenW.argtypes = [HWND, ctypes.POINTER(LOGCONTEXT), BOOL]

lib.WTClose.restype = BOOL
lib.WTClose.argtypes = [HCTX]

lib.WTInfoW.restype = UINT
lib.WTInfoW.argtypes = [UINT, UINT, LPVOID]

lib.WTPacket.restype = BOOL
lib.WTPacket.argtypes = [HCTX, UINT, LPVOID]

lib.WTGetW.restype = BOOL
lib.WTGetW.argtypes = [HCTX, BOOL]


def _WTInfo_size(category: int, index: int) -> int:
    return lib.WTInfoW(category, index, None)

def WTInfo(
        category: int,
        index: int,
        output: ctypes.Structure
        ) -> ctypes.Structure:
    """
    https://developer-docs.wacom.com/docs/icbt/windows/wintab/wintab-reference/#wtinfo

    Parameters
    ----------
    @param category Which category to request information from
    @param index Which information from the category
    @param output A buffer to hold the information
    """

    size = _WTInfo_size(category, index)

    if (size > ctypes.sizeof(output)):
        raise Exception("Requested information is bigger than the provided output buffer.")
    
    lib.WTInfoW(category, index, ctypes.byref(output))
    return output

def WTInfo_string(category: int, index: int) -> str:
    """
    @ref WTInfo but request string (TCHAR[]) information.
    """

    size = _WTInfo_size(category, index)

    buffer = ctypes.create_unicode_buffer(size)
    WTInfo(category, index, buffer)
    return buffer.value

def WTInfo_uint(category: int, index: int) -> int:
    """
    @ref WTInfo but request unsigned integer (UINT) information.
    """

    buffer = UINT()
    WTInfo(category, index, buffer)
    return buffer.value

def get_device_count() -> int:
    """ Get the number of current tablet devices available. """

    return WTInfo_uint(WTI.INTERFACE, IFC.NDEVICES)


class WinTabDevice:
    """
    Class representing a basic WinTab device and context.
    """

    def __init__(self, hwnd: int, index: int):
        """
        Parameters
        ----------
        @param hwnd Window handle to create context on
        @param index Device index
        """

        self.device_index = WTI.DEVICES + index

        self.name = WTInfo_string(self.device_index, DVC.NAME).strip()
        self.packet_rate = WTInfo_uint(self.device_index, DVC.PKTRATE)

        npressure_axis = WTInfo(self.device_index, DVC.NPRESSURE, AXIS())
        self.pressure_min = npressure_axis.axMin
        self.pressure_max = npressure_axis.axMax

        self._context_info = LOGCONTEXT()
        WTInfo(WTI.DEFSYSCTX, 0, self._context_info)

        # This has to match the PACKET structure
        self._context_info.lcPktData = (
            PK.CHANGED | PK.X | PK.Y | PK.Z |
            PK.NORMAL_PRESSURE | PK.TANGENT_PRESSURE | PK.ORIENTATION
        )
        
        self._context_info.lcPktMode = 0 # Absolute mode
        self._context_info.lcOptions |= 0x0004 # CXO_MESSAGES
        self._context_info.lcMsgBase = 0x7ff0 # WT_DEFBASE

        self.context = lib.WTOpenW(hwnd, ctypes.byref(self._context_info), True)
        if not self.context:
            raise Exception("Couldn't open tablet context.")

    def close(self):
        """ Close the device context. """

        lib.WTClose(self.context)