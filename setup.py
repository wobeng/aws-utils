from distutils.core import setup

setup(
    name='aws-utils',
    version='1.0.0',
    packages=['aws_utils'],
    url='https://github.com/wobeng/aws-utils',
    license='',
    author='wobeng',
    author_email='wobeng@yblew.com',
    description='aws utility functions',
    install_requires=[
        'boto3',
        'requests_aws4auth',
        'requests'
    ],
    dependency_links=['git+https://git@github.com/wobeng/py-utils.git@master']
)
