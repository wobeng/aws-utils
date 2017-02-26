import ast
from setuptools.command.install import install
import re,sys
from setuptools import setup, find_packages
from subprocess import call

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

class my_install(install):
    def run(self):
        install.run(self)
        cmd = [sys.executable.replace("python","pip"), "install", "git+https://git@github.com/wobeng/graphics-helper.git@master"]
        call(cmd)

setup(
    name='aws-helper',
    description='aws helper',
    url=_lu_meta['url'],
    author='Welby Obeng',
    license=_lu_meta['license'],
    keywords='aws helper',
    packages=find_packages(),
    version=_lu_meta['version'],
    cmdclass={'install': my_install},
)
