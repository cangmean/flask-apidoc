from setuptools import setup, find_packages

version = '0.1'

setup(
    name="flask-apidoc",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    author='cangmean',
    url='https://github.com/cangmean/flask-apidoc',
    install_requires=[
        'flask', 'pyyaml'
    ],
)