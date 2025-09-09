from setuptools import setup
from setuptools.command.build_py import build_py as build_py_orig
import os
import sys
import subprocess

class build_py(build_py_orig):
    def run(self):
        # Custom build logic for the C library (as before)
        this_dir = os.path.abspath(os.path.dirname(__file__))
        model_dir = os.path.join(this_dir, "pyzbc2014", "model")
        so_name = "libzbc2014"
        ext = {
            "linux": ".so",
            "darwin": ".so",
            "win32": ".dll"
        }[sys.platform if sys.platform != "darwin" else "darwin"]

        lib_path = os.path.join(model_dir, so_name + ext)
        sources = [
            os.path.join(model_dir, "complex.c"),
            os.path.join(model_dir, "model_IHC.c"),
            os.path.join(model_dir, "model_Synapse.c"),
        ]


        if not os.path.exists(lib_path):
            print(f"Compiling C library: {' '.join(sources)} -> {lib_path}")
            if sys.platform == "win32":
                cmd = [
                    "gcc", "-shared", "-O3", "-o", lib_path, *sources
                ]
            else:
                cmd = [
                    "gcc", "-fPIC", "-O3", "-shared", "-o", lib_path, *sources
                ]
            subprocess.check_call(cmd)

        super().run()

setup(
    cmdclass={"build_py": build_py},
    include_package_data=True,
    package_data={
        "pyzbc2014.model": ["libzbc2014.*"]
    },
    zip_safe=False,
)