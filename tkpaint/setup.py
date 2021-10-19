import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("paint.pyw", base=base, target_name="Tk-Paint.exe", icon="logo.ico")]

includefile = ["asset/"]

include = ["atexit"]

exclude = ["logo.ico"]

pkgmodule = ["PIL"]

options = {"build_exe": {"includes":include, "packages": pkgmodule, 'include_files':includefile, 'excludes': exclude}}

setup(
    name="Tk paint",
    version="0.1",
    description="Paint app in Tk",
    options=options,
    executables=executables,
)
