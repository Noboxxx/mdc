import types
import time
import os
import json
import getpass
from mprint import *


def listdir(path, sort=True, full=False):
    ls = list()
    for item in os.listdir(path):
        if full is True:
            item = join_path(path, item)
        ls.append(item)
    if sort is True:
        ls.sort()
    return ls


def join_path(*args):
    return '/'.join(args)


def split_path(path):
    return path.split('/')


def copy(path, destination):
    path_name = split_path(path)[-1]
    new_path = join_path(destination, path_name)
    if os.path.isfile(path):
        with open(path, 'r') as f:
            content = f.read()
        with open(new_path, 'w') as f:
            f.write(content)
    elif os.path.isdir(path):
        os.mkdir(new_path)
        for directory in listdir(path, full=True):
            copy(directory, new_path)


class Builder(object):

    def __init__(self):
        self.steps = list()

    def __iter__(self):
        return iter(self.steps)

    def add_step(self, callable_):
        if not isinstance(callable_, types.FunctionType) and not isinstance(callable_, types.MethodType):
            warning('The given item is not of type \'function\' or \'instancemethod\'. Got -> \'{0}\' of type -> \'{1}\'. Skipping...'.format(callable_, type(callable_)), prefix=self.__class__.__name__)
            return
        self.steps.append(callable_)

    def run(self):
        start_build = time.time()
        info('Build starts', prefix=self.__class__.__name__, new_line_after=True)
        steps_names = '{0} > {1}'.format('Registered steps in order ({0})'.format(len(self.steps)), ', '.join([step.__name__ for step in self.steps]))
        info(steps_names, prefix=self.__class__.__name__, new_line_after=True)
        for step in self:
            start = time.time()
            info('Step \'{0}\' starts'.format(step.__name__), prefix=self.__class__.__name__)
            step()
            info('Step \'{0}\' ends'.format(step.__name__), prefix=self.__class__.__name__, suffix='Took {0} sec.'.format(time.time() - start), new_line_after=True)
        info('Build ends', prefix=self.__class__.__name__, suffix='Took {0} sec.'.format(time.time() - start_build), new_line_after=True)


class Path(object):
    def __init__(self, path):
        if not self.is_one(path):
            error('The given argument(s) is(are) not valid. Got -> {0}'.format(path), prefix=self.__class__.__name__)
        self.path = path

    def __str__(self):
        return self.path

    def __repr__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, self.path)

    @classmethod
    def is_one(cls, path):
        return os.path.exists(path)

    def get_path(self):
        return self.path


class Folder(Path):

    @classmethod
    def is_one(cls, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                return True
        return False

    @classmethod
    def create(cls, path):
        if cls.is_one(path) is True:
            error('Already exists')

        os.mkdir(path)
        return cls(path)

    def get_children(self):
        children = list()
        for path in listdir(self.path, full=True):
            if self.is_one(path):
                children.append(self.__class__(path))
            elif File.is_one(path):
                children.append(File(path))
        return children


class File(Path):
    @classmethod
    def is_one(cls, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                return True
        return False

    @classmethod
    def create(cls, path):
        if cls.is_one(path) is True:
            error('Already exists')

        with open(path, 'w') as f:
            f.write('')

        return cls(path)

    def write(self, content):
        with open(self.path, 'w') as f:
            f.write(content)

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()


class Workspace(Folder):

    @classmethod
    def get_current(cls):
        return cls(cmds.workspace(rootDirectory=True)[:-1])

    @classmethod
    def is_one(cls, path):
        return True

    def get_data(self):
        data = list()
        for path in listdir(self.path, full=True):
            if self.is_one(path):
                data.append(Data(path))
        return data

    def get_name(self):
        return split_path(self.path)[-1]


class Data(Folder):

    @classmethod
    def is_one(cls, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                return True
        return False

    @classmethod
    def create(cls, path):
        if cls.is_one(path) is True:
            error('The data folder already exists therefore it cannot be created -> {0}'.format(path))
        os.mkdir(path)
        return cls(path)

    def get_last_version(self):
        last_data_version = -1
        for data_version in self.get_versions():
            last_data_index = last_data_version.get_index() if isinstance(last_data_version, Version) else -1
            if data_version.get_index() > last_data_index:
                last_data_version = data_version
        if isinstance(last_data_version, Version):
            return last_data_version
        return None

    def get_files(self):
        directories = list()
        for directory in listdir(self.path):
            path = join_path(self.path, directory)
            if directory != Version.__class__.__name__.lower():
                if directory != VersionInfo.name:
                    directories.append(path)
        return directories

    def create_version(self):
        return Version.create(self)

    def empty_folder(self):
        for path in self.get_files():
            os.remove(path)

    def get_versions(self):
        return Version.get_all(self)

    def import_(self):
        error('Import not implemented for this data.', prefix=self.__class__.__name__)

    def export(self):
        error('Export not implemented for this data.', prefix=self.__class__.__name__)

    def get_type(self):
        return split_path(self.path)[-1]


class Version(Folder):

    @classmethod
    def create(cls, data):
        last_version = data.get_last_version()
        index = 0
        if last_version is not None:
            index = last_version.get_index() + 1

        version_path = join_path(data.get_old_path(), str(index))
        os.mkdir(version_path)

        version = cls(version_path)

        for path in data.get_files():
            copy(path, version.get_path())

        VersionInfo.create(version_path)
        return version

    @classmethod
    def is_one(cls, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                if split_path(path)[-1].isdigit():
                    return True
        return False

    @classmethod
    def get_all(cls, data):
        data_versions = list()
        for directory in listdir(data.get_path()):
            if directory.isdigit():
                path = join_path(data.get_path(), directory)
                if Version.is_one(path):
                    data_versions.append(Version(path))
        return data_versions

    def get_index(self):
        split = split_path(self.path)
        return int(split[-1])

    def get_data_type_str(self):
        split = split_path(self.path)
        return int(split[-2])

    def get_files(self):
        paths = list()
        for directory in listdir(self.path):
            paths.append(join_path(self.path, directory))
        return paths


class VersionInfo(File):
    name = 'info.json'

    def get_dict(self):
        with open(self.path) as f:
            content = json.load(f)
        return content

    def get_user(self):
        return self.get_dict()['user']

    def get_creation_date(self):
        return self.get_dict()['creation_date']

    @classmethod
    def create(cls, directory):
        content = {'user': getpass.getuser(), 'creation_date': time.time()}
        info_path = join_path(directory, cls.name)
        if not os.path.exists(info_path):
            with open(info_path, 'w') as f:
                json.dump(content, f)
        return cls(info_path)

    @classmethod
    def is_one(cls, path):
        if os.path.exists(path):
            if os.path.isfile(path):
                if split_path(path)[-1] == cls.name:
                    return True
        return False
