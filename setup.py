from setuptools import setup
from setuptools.command.build_py import build_py as build_py_orig
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
import subprocess
import sys
import os
import shutil

class build_py(build_py_orig):
    def run(self):
        # Path to C sources and output so/dll file
        this_dir = os.path.abspath(os.path.dirname(__file__))
        model_dir = os.path.join(this_dir, "pyzbc2014", "model")
        so_name = "libzbc2014"
        if sys.platform == "win32":
            ext = ".dll"
        else:
            ext = ".so"
        so_path = os.path.join(model_dir, so_name + ext)
        sources = [
            os.path.join(model_dir, "complex.c"),
            os.path.join(model_dir, "model_IHC.c"),
            os.path.join(model_dir, "model_Synapse.c"),
        ]

        if not os.path.exists(so_path):
            print("Compiling C library for pyzbc2014...")
            if sys.platform == "win32":
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

        super().run()

class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False  # This makes the wheel platform-specific

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
    cmdclass={
        "build_py": build_py,
        "bdist_wheel": bdist_wheel,
    },
)