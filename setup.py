from setuptools import setup

setup(
    name="pyzbc2014",
    version="0.0.1",
    author="Daniel Guest",
    author_email="daniel_guest@urmc.rochester.edu",
    packages=["pyzbc2014"],
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0"
    ],
    include_package_data=True,
    package_data={
        'pyzbc2014': ['pyzbc2014/model/libzbc2014.so'],
    },
)
