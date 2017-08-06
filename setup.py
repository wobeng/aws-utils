import sys
from subprocess import call

import os
from setuptools import setup, find_packages
from setuptools.command.install import install


class MyInstall(install):
    def run(self):
        install.run(self)
        requirements_file = os.path.join(os.getcwd(), "requirements.txt")
        if os.path.isfile(requirements_file):
            cmd = [sys.executable.replace("python", "pip"), "install", "-r", requirements_file]
            call(cmd)


setup(
    name='aws-utils',
    description='aws utils',
    author='Welby Obeng',
    keywords='aws utils',
    packages=find_packages(),
    cmdclass={'install': MyInstall},
    install_requires=[
        'boto3',
        'requests_aws4auth',
        'requests'
    ],
    dependency_links=['git+https://git@github.com/wobeng/py-utils.git@master']
)
