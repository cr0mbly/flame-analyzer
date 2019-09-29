import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
INSTALL_REQUIREMENTS = ['Django', 'IPYTHON']

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='publons-flame',
    version='0.1',
    packages=['publons_flame'],
    include_package_data=True,
    license='MIT License',
    description='A small Django and IPython compatible application for benchmarking database and IO heavy work.',
    long_description=README,
    url='https://github.com/pulbons/publons-flame',
    author='Matthew Betts, Aidan Houlihan',
    author_email='aidan@publons.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
