============
artifact-cli
============

Private Artifact Manager using Amazon S3

.. image:: https://badge.fury.io/py/artifact-cli.svg
   :target: http://badge.fury.io/py/artifact-cli
   :alt: PyPI version

.. image:: https://travis-ci.org/mogproject/artifact-cli.svg?branch=master
   :target: https://travis-ci.org/mogproject/artifact-cli
   :alt: Build Status


.. image:: https://coveralls.io/repos/mogproject/artifact-cli/badge.png?branch=master
   :target: https://coveralls.io/r/mogproject/artifact-cli?branch=master
   :alt: Coverage Status

.. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
   :target: http://choosealicense.com/licenses/apache-2.0/
   :alt: License

--------
Features
--------

* Easy & lightweight artifact manager for Java/Scala

  * Optimized for all-in-one packages (e.g., the product of ``sbt dist`` or ``sbt assembly``)

* No database or extra servers needed other than Amazon S3
* Simple command-line interface (CLI)
* Integrates your daily build & deploy tasks

------------
Dependencies
------------

* Python 3.7+

  * Python 2 support was dropped with Version 0.1.11.
  
* pytz
* python-dateutil < 2.8.1, >= 2.1
* GitPython >= 0.3.5
* boto3
* botocore
* moto (for testing)

------------
Installation
------------

* ``pip`` command may require ``sudo``

+-------------------------+------------------------------------------+
| Operation               | Command                                  |
+=========================+==========================================+
| Install                 |``pip install artifact-cli``              |
+-------------------------+------------------------------------------+
| Upgrade                 |``pip install --upgrade artifact-cli``    |
+-------------------------+------------------------------------------+
| Uninstall               |``pip uninstall artifact-cli``            |
+-------------------------+------------------------------------------+
| Check installed version |``art --version``                         |
+-------------------------+------------------------------------------+
| Help                    |``art -h``                                |
+-------------------------+------------------------------------------+

----------------
Quickstart Guide
----------------

1. Create your Amazon Web Services account (if needed)
------------------------------------------------------

The charge on your AWS account is your responsibility.

2. Create IAM User to access Amazon S3 (if needed)
--------------------------------------------------

Manage your own **access key ID** and **secret access key** to call the APIs.

3. Create Amazon S3 bucket
--------------------------

Add permissions to the IAM user.

4. Make configuration file
--------------------------

Create the file ``~/.artifact-cli`` and include credential information for AWS like this:

.. code-block:: ini

    [default]
    aws_access_key_id = XXXXXXXXXXXXXXXXXXXX
    aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    bucket = your-bucket-name
    region = your-region (e.g. ap-northeast-1, us-east-1)

You may override those settings by command-line options and/or environment variables.

* Command-line Options (will override the settings from environment variables)

+--------------------------+-------------------------------------+
| Option                   | Description                         |
+==========================+=====================================+
| ``--access ACCESS_KEY``  | AWS access key.                     |
+--------------------------+-------------------------------------+
| ``--secret SECRET_KEY``  | AWS secret key.                     |
+--------------------------+-------------------------------------+
| ``--bucket BUCKET_NAME`` | S3 bucket name.                     |
+--------------------------+-------------------------------------+
| ``--region REGION``      | Region name of the S3 bucket.       |
+--------------------------+-------------------------------------+

* Environment Variables

+---------------------------+-------------------------------------+
| Variable Name             | Description                         |
+===========================+=====================================+
| ``AWS_ACCESS_KEY_ID``     | AWS access key.                     |
+---------------------------+-------------------------------------+
| ``AWS_SECRET_ACCESS_KEY`` | AWS secret key.                     |
+---------------------------+-------------------------------------+
| ``AWS_DEFAULT_REGION``    | Region name of the S3 bucket.       |
+---------------------------+-------------------------------------+

5. Check connection
-------------------

Now, you are ready for the ``art`` command.
Let's try to list your artifacts::

    $ art list GROUP_ID
    [INFO] No artifacts.

You'll see, there are no artifacts!

6. Build the artifact
---------------------

Build is something outside of this tool. In other words, you can build as you like.

7. Upload the artifact
----------------------

In the builder's environment, you can upload the artifact to Amazon S3::

    $ art upload GROUP_ID /path/to/your-artifact-0.0.1.jar

Specify group id and your local file path.

| Artifact ID, version, and packaging(=extension) are automatically parsed from the given file name.
| In this case, artifact ID is ``your-artifact``, version is ``0.0.1`` and packaging is ``jar``.

8. View the artifact information
--------------------------------

To view the index data, run ``art list`` or ``art info``.

9. Download the artifact
------------------------

Login to the deployer's environment, then download the artifact from Amazon S3::

    $ art download GROUP_ID /path/to/deployers/your-artifact-0.0.1.jar 1

To download the latest revision, use ``latest`` keyword. (case-sensitive)::

    $ art download GROUP_ID /path/to/deployers/your-artifact-0.0.1.jar latest

10. Deploy
----------

Deploy the artifact in any way you like!

11. And then ...
----------------

For further information, type ``art -h``.

---------------
Amazon S3 Paths
---------------

The structure of the paths is the following::

    your-bucket-name
    ├── group.id.1                          // group ID
    │   ├── .meta                           // meta data directory for each group
    │   │   ├── index-awesome-project.json  // index data is written as JSON for each artifact ID
    │   │   └── index-play-project.json
    │   ├── awesome-project                 // artifact ID
    │   │   ├── 0.0.1                       // version
    │   │   │   ├── 1                       // revision (auto assigned, starting from 1)
    |   │   │   │   └── awesome-project-0.0.1.jar
    |   │   │   ├── 2
    |   │   │   │   └── awesome-project-0.0.1.jar
    |   │   │   ├── 3
    |   │   │   │   └── awesome-project-0.0.1.jar
    |   │   │   └── 4
    |   │   │       └── awesome-project-0.0.1.jar
    │   │   └── 0.0.2-SNAPSHOT
    │   │       ├── 1
    |   │       │   └── awesome-project-0.0.2-SNAPSHOT.jar
    |   │       └── 2
    |   │           └── awesome-project-0.0.2-SNAPSHOT.jar
    │   └── play-project
    │       └── 0.0.1
    │           └── 1
    |               └── play-project-0.0.1.zip
    └── group.id.2
        ├── .meta
        │   └── index-awesome-project.json
        └── awesome-project                 // completely separated to the group.id.1's artifact
            └── 0.0.1
                └── 1
                    └── awesome-project-0.0.1.zip

-----
Notes
-----

* This tool supports only artifact-id-level concurrency.

  * Simultaneous uploading of the artifacts with the same artifact id may break your repository.

