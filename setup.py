from setuptools import setup, find_packages

setup(
    name='aws-utils',
    version='1.0.0',
    packages=find_packages(exclude=['tests', 'tests.*']),
    url='https://github.com/wobeng/aws-utils',
    license='',
    author='wobeng',
    author_email='wobeng@yblew.com',
    description='aws utility functions',
    install_requires=[
        'boto3',
        'requests_aws4auth',
        'requests',
        'cryptography',
        'simplejson',
        'pytz'
    ]
)
