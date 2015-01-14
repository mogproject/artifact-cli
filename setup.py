from setuptools import setup, find_packages

SRC_DIR = 'src'


def get_version():
    import sys

    sys.path[:0] = [SRC_DIR]
    return __import__('artifactcli').__version__


def get_requirements(path):
    import os

    with open(path) as f:
        return f.read().splitlines()

setup(
    name='artifact-cli',
    version=get_version(),
    description='Private Artifact Manager using Amazon S3',
    author='mogproject',
    author_email='mogproj@gmail.com',
    url='https://github.com/mogproject/artifact-cli',
    install_requires=get_requirements('requirements.txt'),
    tests_require=get_requirements('test-requirements.txt'),
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR),
    include_package_data=True,
    test_suite='tests',
    entry_points="""
    [console_scripts]
    art = artifactcli.artifactcli:main
    """,
)
