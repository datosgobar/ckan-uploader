# coding=utf-8
from setuptools import setup, find_packages
import os

here = os.path.dirname(__file__)
requirements_file = os.path.join(here, 'requirements.txt')

with open(requirements_file) as f:
    requirements = [req.strip() for req in f.readlines()]

setup(
    name='ckan_uploader',
    version='0.1.1',
    packages=find_packages(),
    description='Carga y actualizacion de recursos remotos en una plataforma CKAN 2.5.3+',
    long_description='Librería de python para la carga y actualizacion '
                     'de recursos remotos en una plataforma CKAN 2.5.3+',
    author='Jose A. Salgado',
    author_email='jose.salgado.wrk@gmail.com',
    url='https://github.com/datosgobar/ckan-uploader',
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    download_url='https://github.com/datosgobar/ckan-uploader/releases/tag/rc1.0',
    keywords='ckan-uploader ckan resources',
    entry_points="""""",
)