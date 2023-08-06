

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='novigi_common',
    version="1.0.8",
    description='Novigi Custom Airflow operators, hooks and plugins',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT', 
    packages=['novigi_common','novigi_common.operators', 'novigi_common.hooks', 'novigi_common.custom_plugings', 'novigi_common.utils'],
    install_requires=['requests','jsonpath_ng','pandas'],
    setup_requires=['setuptools', 'wheel'],
    author='Novigi',
    author_email='integration@novigi.com.au',
)
