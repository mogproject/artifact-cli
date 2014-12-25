from setuptools import setup, find_packages

setup(
    name='artifact-cli',
    version='0.0.3',
    description='Private Artifact Manager using Amazon S3',
    author='mogproject',
    author_email='mogproj@gmail.com',
    url='http://about.me/mogproject',
    install_requires=[
        'pytz',
        'python-dateutil',
        'GitPython',
        'boto',
    ],
    tests_require=[
        'moto',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    test_suite='tests',
    entry_points="""
    [console_scripts]
    art = artifactcli.artifactcli:main
    """,
)
