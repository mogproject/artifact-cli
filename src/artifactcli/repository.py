import json
import logging
import sys
from copy import deepcopy
from collections import defaultdict
from artifact import Artifact, BasicInfo
from util import *


class Repository(CaseClass):
    def __init__(self, driver, group_id):
        super(Repository, self).__init__(['driver', 'group_id', 'artifacts'])
        self.driver = driver
        self.group_id = group_id
        self.artifacts = defaultdict(list)

    def load(self, artifact_id):
        """
        Load artifacts index for specified artifact id from storage

        :param artifact_id: artifact id to load
        :return: None
        """
        s = self.driver.read_index(artifact_id)
        xs = json.loads(s, encoding='utf-8') if s else []
        self.artifacts[artifact_id] = [Artifact.from_dict(x) for x in xs]

    def load_all(self):
        """
        Load all artifacts index from storage

        :return: None
        """
        self.artifacts = defaultdict(list)
        for artifact_id in self.driver.artifact_ids():
            self.load(artifact_id)

    def save(self, artifact_id):
        """
        Persist current artifacts index for specified artifact id to storage

        :param artifact_id: artifact id to save
        :return: None
        """
        xs = [x.to_dict() for x in self.artifacts[artifact_id]]
        s = json.dumps(xs, ensure_ascii=False)
        self.driver.write_index(artifact_id, to_unicode(s))

    def upload(self, local_path, artifact=None, force=False, print_only=False):
        """
        Upload local artifact and update index

        :param local_path: source file path to upload
        :param artifact: artifact object to upload
                         If artifact is None, generate artifact object from local_path.
                         Revision will be updated.
        :param force:
        :param print_only:
        :return: None
        """
        art = deepcopy(artifact)
        if not artifact:
            art = Artifact.from_path(self.group_id, local_path)

        bi = art.basic_info
        fi = art.file_info

        # check if the artifact is already in index
        revisions = self._get_artifacts(bi.artifact_id, bi.version, bi.packaging)
        xs = [x for x in revisions if (x.file_info.size, x.file_info.md5) == (fi.size, fi.md5)]
        if xs and not force:
            logging.warn('Already uploaded as:\n%s' % xs[0])
            return

        # increment revision
        latest = self._get_latest_artifact(bi.artifact_id, bi.version, bi.packaging)
        current_revision = latest[0].basic_info.revision if latest else 0
        bi.revision = current_revision + 1

        # upload file
        if print_only:
            logging.info('Would upload artifact: \n\n%s\n' % art)
            return

        logging.info('Uploading artifact: \n%s\n' % art)
        self.driver.upload(local_path, bi.s3_path(), fi.md5)

        # update index
        self.artifacts[bi.artifact_id].append(art)

    def download(self, local_path, revision=None, print_only=False):
        """
        Download specified artifact from repository

        :param local_path: destination path (including file name)
                           artifact id, version and packaging is parsed from the file name
        :param revision: revision to download
                         if revision is None, download latest revision
        :param print_only:
        :return: None
        """
        art = self._get_artifact_from_path(local_path, revision)

        # download file
        if print_only:
            logging.info('Would download artifact: \n\n%s\n' % art)
            return

        logging.info('Downloading artifact: \n%s\n' % art)
        self.driver.download(art.basic_info.s3_path(), local_path, art.file_info.md5)

    def delete(self, file_name, revision, print_only=False):
        """
        Delete specified artifact from repository

        :param file_name: file name of the artifact
                          artifact id, version and packaging is parsed from the file name
        :param revision: revision to delete (should not be none)
        :param print_only:
        :return: None
        """
        if revision is None:
            raise ValueError('Revision should be specified to delete.')
        art = self._get_artifact_from_path(file_name, revision)
        bi = art.basic_info

        # delete file
        if print_only:
            logging.info('Would delete artifact: \n\n%s\n' % art)
            return

        logging.info('Deleting artifact: \n%s\n' % art)
        self.driver.delete(bi.s3_path(), art.file_info.md5)

        # update index
        self._del_artifacts(bi.artifact_id, bi.version, bi.packaging, revision)

    def print_list(self, output=None, fp=sys.stdout):
        output = output or 'text'
        arts = sorted(x for xs in self.artifacts.values() for x in xs)
        if not arts:
            logging.info('No artifacts.')
            return

        buf = []
        if output == 'text':
            headers = ['FILE', '  #', 'SIZE', 'BUILD', 'TAGS', 'SUMMARY']
            values = [
                [
                    '%s-%s.%s' % (x.basic_info.artifact_id, x.basic_info.version, x.basic_info.packaging),
                    '%4.d' % x.basic_info.revision,
                    x.file_info.size_format(),
                    '%s' % x.file_info.mtime,
                    ','.join(x.scm_info.tags) if x.scm_info else '',
                    x.scm_info.summary if x.scm_info else '',
                ] for x in arts]
            column_len = [max([unicode_width(x) + 2 for x in xs]) for xs in zip(*([headers] + values))]
            header_line = ' '.join(unicode_ljust(s, x) for s, x in zip(headers, column_len))
            buf += [header_line, '-' * len(header_line)]
            buf += (' '.join(unicode_ljust(s, x) for s, x in zip(v, column_len)) for v in values)
        elif output == 'json':
            buf.append(json.dumps([x.to_dict() for x in arts], ensure_ascii=False))
        else:
            raise ValueError('Unknown output format: %s' % output)

        for line in buf:
            fp.write(to_str(line) + '\n')

    def print_info(self, file_name, revision=None, output=None, fp=sys.stdout):
        output = output or 'text'
        art = self._get_artifact_from_path(file_name, revision)

        if output == 'text':
            s = str(art)
        elif output == 'json':
            s = json.dumps(art.to_dict(), ensure_ascii=False)
        else:
            raise ValueError('Unknown output format: %s' % output)
        fp.write(to_str(s) + '\n')

    def _get_artifact_from_path(self, path, revision=None):
        bi = BasicInfo.from_path(self.group_id, path)
        return self._get_artifact(bi.artifact_id, bi.version, bi.packaging, revision)

    def _get_artifact(self, artifact_id, version, packaging, revision=None):
        if revision is None:
            arts = self._get_latest_artifact(artifact_id, version, packaging)
        else:
            arts = self._get_artifacts(artifact_id, version, packaging, revision)

        # check if the revision is available
        if len(arts) == 0:
            raise ValueError(
                'No such artifact: driver=%s, artifact_id=%r, version=%r, packaging=%r, revision=%r'
                % (self.driver, artifact_id, version, packaging, revision))
        if len(arts) >= 2:
            raise ValueError(
                'Found duplicated revision (index may be broken): '
                'driver=%s, artifact_id=%r, version=%r, packaging=%r, revision=%r'
                % (self.driver, artifact_id, version, packaging, revision))
        return arts[0]

    @classmethod
    def _match_artifact(cls, artifact, artifact_id=None, version=None, packaging=None, revision=None):
        return ((artifact_id is None or artifact.basic_info.artifact_id == artifact_id)
                and (version is None or artifact.basic_info.version == version)
                and (packaging is None or artifact.basic_info.packaging == packaging)
                and (revision is None or artifact.basic_info.revision == revision))

    def _get_artifacts(self, artifact_id=None, version=None, packaging=None, revision=None):
        return [
            x for xs in self.artifacts.values() for x in xs
            if self._match_artifact(x, artifact_id, version, packaging, revision)
        ]

    def _del_artifacts(self, artifact_id, version, packaging, revision):
        self.artifacts[artifact_id] = [
            x for x in self.artifacts[artifact_id]
            if not self._match_artifact(x, artifact_id, version, packaging, revision)
        ]

    def _get_latest_artifact(self, artifact_id, version, packaging):
        ret = self._get_artifacts(artifact_id, version, packaging)
        return [max(ret, key=lambda x: x.basic_info.revision)] if ret else []
