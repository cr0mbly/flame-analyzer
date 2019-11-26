import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='flame-analyzer',
    version='0.1.5',
    packages=find_packages(
        include=['flame_analyzer'], exclude=('tests')
    ),
    package_data={'flame_analyzer': ['*.pl']},
    include_package_data=True,
    license='MIT License',
    long_description=README,
    description=(
        'A small Django and IPython compatible application for benchmarking '
        'database and IO heavy work.'
    ),
    url='https://github.com/publons/flame-analyzer',
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
