artifact-cli
============

Private Artifact Manager using Amazon S3

[![Build Status](https://travis-ci.org/mogproject/artifact-cli.svg?branch=master)](https://travis-ci.org/mogproject/artifact-cli)
[![Coverage Status](https://img.shields.io/coveralls/mogproject/artifact-cli.svg)](https://coveralls.io/r/mogproject/artifact-cli?branch=master)
[![Stories in Ready](https://badge.waffle.io/mogproject/artifact-cli.png?label=ready&title=Ready)](https://waffle.io/mogproject/artifact-cli)


### Features

- Easy & lightweight artifact manager for Java/Scala
    - Especially optimized for all-in-one package (e.g. the result of ```sbt dist``` or ```sbt assembly```)
- No database or extra servers needed except Amazon S3
- Quite simple command line interface (CLI)
- Integrate your daily build & deploy tasks


### Dependencies

- Python >= 2.6
- pytz
- python-dateutil
- GitPython
- boto
- moto (for testing)


### Installation

Just install via pip! (may need ```sudo``` command)

```
pip install artifact-cli
```

### Upgrading

```
pip install --upgrade artifact-cli
art --version
```

### Quickstart Guide

#### 1. Create your Amazon Web Services account (if need)

The responsibility of the AWS's charge is your own.

#### 2. Create IAM User to access Amazon S3 (if need)

Manage your own **access key ID** and **secret access key** to call the APIs.

#### 3. Create Amazon S3 bucket

Set permissions to the IAM user.

#### 4. Make configuration file

Create ```~/.artifact-cli``` file and write credentials for AWS like this.

```
[default]
aws_access_key_id = XXXXXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
bucket = your-bucket-name
region = your-region (e.g. ap-northeast-1, us-east-1)
```

Or you can use command line options instead of the configuration file.  
(```--access ACCESS_KEY --secret SECRET_KEY --bucket BUCKET_NAME --region REGION```)

#### 5. Check connection

Now, you are ready for using ```art``` command in the shell.  
Just list your artifacts.

```
$ art list GROUP_ID
[INFO] No artifacts.
```

Of course, there are no artifacts!

#### 6. Build the artifact

Building is outside the reach of this tool.  
In other words, you can build as you like.

#### 7. Upload the artifact

In the builder's environment, you can upload the artifact to Amazon S3.

```
$ art upload GROUP_ID /path/to/your-artifact-0.0.1.jar
```

Specify group id and your local file path.

Artifact ID, version and packaging(=extension) are automatically parsed from the given file name.  
In this case, artifact ID is ```your-artifact```, version is ```0.0.1``` and packaging is ```jar```.

#### 8. View the artifact information

To view the index data, run ```art list``` or ```art info```.

#### 9. Download the artifact

Login to the deployer's environment, then download the artifact from Amazon S3.

```
$ art download GROUP_ID /path/to/deployers/your-artifact-0.0.1.jar 1
```

To download the latest revision, use ```latest``` keyword. (case-sensitive)

```
$ art download GROUP_ID /path/to/deployers/your-artifact-0.0.1.jar latest
```

#### 10. Deploy

Deploy the artifact any way you like!

#### 11. And then ...

For further information, type ```art -h```.


### Amazon S3 Paths

The structure of the paths is the following.

```
your-bucket-name
├── group.id.1                     // group ID
│   ├── artifact-cli-index.json    // Index data is written as JSON in each group's directory
│   ├── awesome-project            // artifact ID
│   │   ├── 0.0.1                  // version
│   │   │   ├── 1                  // revision (auto assigned, starting from 1)
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
    ├── artifact-cli-index.json
    └── awesome-project            // completely separated to the group.id.1's artifact
        └── 0.0.1
            └── 1
                └── awesome-project-0.0.1.zip
```


### Uninstallation

```
pip uninstall artifact-cli
```
