import platform


if platform.system() == "Windows":
    from src.tablet.win32 import Win32Tablet as Tablet
    from src.tablet.win32 import get_count

else:
    ...
    # No interface for other operating systems yet (╥﹏╥)