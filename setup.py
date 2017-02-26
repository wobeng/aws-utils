import ast

import re
from setuptools import setup, find_packages


def package_meta():
    """Read __init__.py for global package metadata.
    Do this without importing the package.
    """
    _version_re = re.compile(r'__version__\s+=\s+(.*)')
    _url_re = re.compile(r'__url__\s+=\s+(.*)')
    _license_re = re.compile(r'__license__\s+=\s+(.*)')

    with open('aws_helper/__init__.py', 'rb') as ffinit:
        initcontent = ffinit.read()
        version = str(ast.literal_eval(_version_re.search(
            initcontent.decode('utf-8')).group(1)))
        url = str(ast.literal_eval(_url_re.search(
            initcontent.decode('utf-8')).group(1)))
        licencia = str(ast.literal_eval(_license_re.search(
            initcontent.decode('utf-8')).group(1)))
    return {
        'version': version,
        'license': licencia,
        'url': url,
    }


_lu_meta = package_meta()

setup(
    name='aws-helper',
    description='aws helper',
    url=_lu_meta['url'],
    author='Welby Obeng',
    license=_lu_meta['license'],
    keywords='aws helper',
    packages=find_packages(),
    version=_lu_meta['version'],
    dependency_links=['git+https://github.com/wobeng/helper.git@master#egg=helper-1.0.0'],
    install_requires = ['helper==1.0.0']
)
