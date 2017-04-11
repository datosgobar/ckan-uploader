# coding=utf-8
from setuptools import setup, find_packages
import shutil
import os

base_folder = os.path.dirname(__file__)
docs_folder = os.path.join(base_folder, 'docs')

with open('index.md') as readme_file:
    readme = readme_file.read()

if not os.path.exists(docs_folder):
    os.makedirs(docs_folder)

shutil.copy("index.md", os.path.join(docs_folder, "index.md"))

with open("requirements.txt") as f:
    requirements = [req.strip() for req in f.readlines()]

setup(
    name='ckan_uploader',
    version='0.1',
    packages=find_packages(),
    description=readme,  # groso beni!
    long_description='',
    author='DatosAr',
    author_email='',
    url='https://github.com/datosgobar/ckan_uploader',
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='ckan_uploader',
    entry_points="""""",
)