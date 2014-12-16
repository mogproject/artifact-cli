import json
from . import Artifact, BasicInfo


class Repository:
    def __init__(self, driver):
        self.driver = driver
        self.artifacts = []

    def load(self):
        """
        Load artifacts index from storage
        :return: None
        """
        s = self.driver.read_index()
        self.artifacts = [Artifact.from_dict(json.loads(x)) for x in s.splitlines()]

    def save(self):
        """
        Persist current artifacts index to storage
        :return: None
        """
        xs = [json.dumps(x.to_dict()) for x in self.artifacts]
        s = '\n'.join(xs)
        self.driver.write_index(s)

    def upload(self, group_id, local_path, artifact=None):
        """
        Upload local artifact and update index
        :param group_id: group id of the artifact
        :param: local_path: source file path to upload
        :param artifact: artifact object to upload
                         If artifact is None, generate artifact object from local_path.
                         Revision will be updated.
        :return: None
        """

        if not artifact:
            artifact = Artifact.from_path(group_id, local_path)

        # check if the artifact is already in index
        bi = artifact.basic_info
        fi = artifact.file_info
        revisions = self.get_artifacts(bi.group_id, bi.artifact_id, bi.version, bi.packaging)
        xs = [x for x in revisions if (x.file_info.size, x.file_info.md5) == (fi.size, fi.md5)]
        if xs:
            raise ValueError('Already uploaded as:\n%s' % xs[0])

        # increment revision
        latest = self.get_latest_artifact(bi.group_id, bi.artifact_id, bi.version, bi.packaging)
        current_revision = latest.basic_info.revision if latest else 0
        bi.revision = current_revision + 1

        # upload file
        print('Uploading artifact: \n%s\n' % artifact)
        self.driver.upload(local_path, bi.s3_path())

        # update index
        self.artifacts.append(artifact)
        self.save()

    def download(self, group_id, local_path, revision=None):
        """
        Download specified artifact from repository
        :param group_id: group id of the artifact
        :param local_path: destination path (including file name)
                           artifact id, version and packaging is parsed from the file name
        :param revision: revision to download
                         if revision is None, download latest revision
        :return: None
        """
        bi = BasicInfo.from_path(group_id, local_path)
        if revision is None:
            arts = self.get_latest_artifact(bi.group_id, bi.artifact_id, bi.version, bi.packaging)
        else:
            arts = self.get_artifacts(bi.group_id, bi.artifact_id, bi.version, bi.packaging, bi.revision)

        # check if the revision is available
        if len(arts) == 0:
            raise ValueError(
                'No such revision: '
                'group_id=%s, artifact_id=%s, version=%s, packaging=%s, revision=%s'
                % (group_id, bi.artifact_id, bi.version, bi.packaging, revision))
        if len(arts) >= 2:
            raise ValueError(
                'Found duplicated revision (index may be broken): '
                'group_id=%s, artifact_id=%s, version=%s, packaging=%s, revision=%s'
                % (group_id, bi.artifact_id, bi.version, bi.packaging, revision))
        art = arts[0]

        # download file
        print('Downloading... %s' % art)
        self.driver.download(art.basic_info.s3_path(), local_path, art.basic_info.md5)

    def print_list(self):
        # TODO: be more pretty
        values = [
            (
                x.basic_info.group_id,
                x.basic_info.artifact_id,
                x.basic_info.version,
                x.basic_info.packaging,
                x.basic_info.revision,
                x.file_info.size,
                x.scm_info.branch,
                x.scm_info.author_name,
                x.scm_info.committed_date,
                x.scm_info.summary,
            ) for x in self.artifacts]
        for v in sorted(values):
            print('%s %s %s %s %s %s %s %s %s %s' % v)

    def get_artifacts(self, group_id, artifact_id=None, version=None, packaging=None, revision=None):
        return [
            x for x in self.artifacts
            if x.basic_info.group_id == group_id
            and (artifact_id is None or x.basic_info.artifact_id == artifact_id)
            and (version is None or x.basic_info.version == version)
            and (packaging is None or x.basic_info.packaging == packaging)
            and (revision is None or x.basic_info.revision == revision)
        ]

    def get_latest_artifact(self, group_id, artifact_id, version, packaging):
        ret = self.get_artifacts(group_id, artifact_id, version, packaging)
        return max(ret, key=lambda x: x.basic_info.revision) if ret else None
