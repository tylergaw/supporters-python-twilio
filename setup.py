import logging
import os
import pip
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import supporters_twilio

logger = logging.getLogger(__name__)

PWD = os.path.abspath(os.path.dirname(__file__))
README_PATH = os.path.join(PWD, 'README.md')
VERSION = supporters_twilio.__version__


def get_readme():
    with open(README_PATH) as readme:
        return readme.read()

REQUIREMENTS = [
    'Flask==0.10.1',
    'gevent==1.0.1',
    'gunicorn==19.3.0',
    'requests==2.7.0',
    'twilio==4.5.0',
]

TEST_REQUIREMENTS = [
    'coverage==3.7.1',
    'mock==1.0.1',
    'pytest==2.6.4',
] + REQUIREMENTS


class RunTests(TestCommand):
    description = 'Install test dependencies and run tests'
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run(self):
        pip_arguments =  ['install'] + TEST_REQUIREMENTS
        pip.main(pip_arguments)
        try:
            import coverage
            import pkgutil
            import pytest
            cov = coverage.coverage(source=['supporters_twilio/'])
            cov.start()
            errno = pytest.main(self.pytest_args)
            cov.stop()
            cov.save()
            cov.html_report(directory='htmlcov')
        except Exception:
            logger.error('-' * 60)
            logger.exception('Exception thrown while running tests')
            logger.error('-' * 60)
        finally:
            sys.exit(errno)


setup(
    name='supporters_twilio',
    version=VERSION,
    description='An example of signing up new Supporters using The Groundwork API through SMS and a Flask Application',
    url='https://github.com/tylergaw/supporters-python-twilio',
    long_description=get_readme(),
    author='The Groundwork',
    author_email='info@thegroundwork.com',
    packages=find_packages(),
    zip_safe=False,
    install_requires=REQUIREMENTS,
    include_package_data=True,
    cmdclass={'test': RunTests},
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ]
)
