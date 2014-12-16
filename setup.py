from setuptools import setup, find_packages

setup(
    name='artima',
    version='0.0.1-SNAPSHOT',
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
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    test_suite='tests',
    entry_points="""
    [console_scripts]
    artima = artima.artima:main
    """,
)
