from setuptools import setup
from setuptools.command.build_py import build_py as build_py_orig
import subprocess
import sys
import os
import shutil

class build_py(build_py_orig):
    def run(self):
        # Path to C sources and output so file
        this_dir = os.path.abspath(os.path.dirname(__file__))
        model_dir = os.path.join(this_dir, "pyzbc2014", "model")
        so_name = "libzbc2014"
        ext = {
            "linux": ".so",
            "darwin": ".so",
            "win32": ".dll"
        }[sys.platform if sys.platform != "darwin" else "darwin"]

        so_path = os.path.join(model_dir, so_name + ext)

        sources = [
            os.path.join(model_dir, "complex.c"),
            os.path.join(model_dir, "model_IHC.c"),
            os.path.join(model_dir, "model_Synapse.c"),
        ]

        if not os.path.exists(so_path):  # Only build if missing or forced
            print("Compiling C library for pyzbc2014...")
            cmd = None
            if sys.platform == "win32":
                # Use mingw32 (assumes gcc available via MSYS2 or similar)
                cmd = [
                    "gcc",
                    "-shared",
                    "-O3",
                    "-o", so_path,
                    *sources
                ]
            else:
                cmd = [
                    "gcc",
                    "-fPIC",
                    "-O3",
                    "-shared",
                    "-o", so_path,
                    *sources
                ]
            subprocess.check_call(cmd)

        # Continue with normal build_py logic
        super().run()

setup(
    name="pyzbc2014",
    version="0.0.2",
    author="Daniel Guest",
    author_email="daniel_guest@urmc.rochester.edu",
    packages=["pyzbc2014", "pyzbc2014.model"],
    install_requires=[
        "setuptools",
        "numpy>=1.21.0",
        "scipy>=1.7.0"
    ],
    include_package_data=True,
    package_data={
        'pyzbc2014': ['model/libzbc2014.*'],
    },
    cmdclass={"build_py": build_py},
)