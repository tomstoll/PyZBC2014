from setuptools import setup, Extension, find_packages
import re
import os


def read_version():  # note: update version in pyzbc2014.__init__
    with open(os.path.join(os.path.dirname(__file__), "pyzbc2014", "__init__.py")) as f:
        m = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', f.read())
    if not m:
        raise RuntimeError("version string not found")
    return m.group(1)


ext_modules = [
    Extension(
        "pyzbc2014.model.libzbc2014",    # This will create a Python extension module in pyzbc2014/model
        sources=[
            "pyzbc2014/model/complex.c",
            "pyzbc2014/model/model_IHC.c",
            "pyzbc2014/model/model_Synapse.c",
            "pyzbc2014/model/stubmodule.c",
        ],
        extra_compile_args=["-O3"],
        # If you have .h files needed, this will work as long as they are in the same directory.
    )
]

setup(
    name="pyzbc2014",
    version=read_version(),
    author="Daniel Guest",
    author_email="daniel_guest@urmc.rochester.edu",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0"
    ],
    ext_modules=ext_modules,
    include_package_data=True,
    zip_safe=False,  # Not strictly needed but sometimes helps with loading .so files
)