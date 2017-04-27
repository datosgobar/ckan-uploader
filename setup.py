# coding=utf-8
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [req.strip() for req in f.readlines()]

setup(
    name='ckan_uploader',
    version='0.1',
    packages=find_packages(),
    description='short description',
    long_description='long description',
    author='DatosAr',
    author_email='',
    url='https://github.com/datosgobar/ckan-uploader',
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    download_url='https://github.com/datosgobar/ckan-uploader/releases/tag/rc1.0',
    keywords='ckan-uploader ckan resources',
    entry_points="""""",
)