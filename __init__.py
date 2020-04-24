from PySide2 import QtWidgets, QtCore
import datetime
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import re
import os
from maya import cmds, mel
import json
import time
import getpass
import sys
import workspace_loader
import webbrowser
import shutil
import types


# import types
# import time
# import os
# import json
# import getpass
# from mprint import *
#
#
# def listdir(path, sort=True, full=False):
#     ls = list()
#     for item in os.listdir(path):
#         if full is True:
#             item = join_path(path, item)
#         ls.append(item)
#     if sort is True:
#         ls.sort()
#     return ls
#
#
# def join_path(*args):
#     return '/'.join(args)
#
#
# def split_path(path):
#     return path.split('/')
#
#
#
#
# class Builder(object):
#
#     def __init__(self):
#         self.steps = list()
#
#     def __iter__(self):
#         return iter(self.steps)
#
#     def add_step(self, callable_):
#         if not isinstance(callable_, types.FunctionType) and not isinstance(callable_, types.MethodType):
#             warning('The given item is not of type \'function\' or \'instancemethod\'. Got -> \'{0}\' of type -> \'{1}\'. Skipping...'.format(callable_, type(callable_)), prefix=self.__class__.__name__)
#             return
#         self.steps.append(callable_)
#
#     def run(self):
#         start_build = time.time()
#         info('Build starts', prefix=self.__class__.__name__, new_line_after=True)
#         steps_names = '{0} > {1}'.format('Registered steps in order ({0})'.format(len(self.steps)), ', '.join([step.__name__ for step in self.steps]))
#         info(steps_names, prefix=self.__class__.__name__, new_line_after=True)
#         for step in self:
#             start = time.time()
#             info('Step \'{0}\' starts'.format(step.__name__), prefix=self.__class__.__name__)
#             step()
#             info('Step \'{0}\' ends'.format(step.__name__), prefix=self.__class__.__name__, suffix='Took {0} sec.'.format(time.time() - start), new_line_after=True)
#         info('Build ends', prefix=self.__class__.__name__, suffix='Took {0} sec.'.format(time.time() - start_build), new_line_after=True)
#
#
# class Path(object):
#     def __init__(self, path):
#         if not self.is_one(path):
#             error('The given argument(s) is(are) not valid. Got -> {0}'.format(path), prefix=self.__class__.__name__)
#         self.path = path
#
#     def __str__(self):
#         return self.path
#
#     def __repr__(self):
#         return '<{0}: {1}>'.format(self.__class__.__name__, self.path)
#
#     @classmethod
#     def is_one(cls, path):
#         return os.path.exists(path)
#
#     def get_path(self):
#         return self.path
#
#
# class Folder(Path):
#
#     @classmethod
#     def is_one(cls, path):
#         if os.path.exists(path):
#             if os.path.isdir(path):
#                 return True
#         return False
#
#     @classmethod
#     def create(cls, path):
#         if cls.is_one(path) is True:
#             error('Already exists')
#
#         os.mkdir(path)
#         return cls(path)
#
#     def get_children(self):
#         children = list()
#         for path in listdir(self.path, full=True):
#             if self.is_one(path):
#                 children.append(self.__class__(path))
#             elif File.is_one(path):
#                 children.append(File(path))
#         return children
#
#
# class File(Path):
#     @classmethod
#     def is_one(cls, path):
#         if os.path.exists(path):
#             if os.path.isfile(path):
#                 return True
#         return False
#
#     @classmethod
#     def create(cls, path):
#         if cls.is_one(path) is True:
#             error('Already exists')
#
#         with open(path, 'w') as f:
#             f.write('')
#
#         return cls(path)
#
#     def write(self, content):
#         with open(self.path, 'w') as f:
#             f.write(content)
#
#     def read(self):
#         with open(self.path, 'r') as f:
#             return f.read()
#
#
# class Workspace(Folder):
#
#     @classmethod
#     def get_current(cls):
#         return cls(cmds.workspace(rootDirectory=True)[:-1])
#
#     @classmethod
#     def is_one(cls, path):
#         return True
#
#     def get_data(self):
#         data = list()
#         for path in listdir(self.path, full=True):
#             if self.is_one(path):
#                 data.append(Data(path))
#         return data
#
#     def get_name(self):
#         return split_path(self.path)[-1]
#
#
# class Data(Folder):
#
#     @classmethod
#     def is_one(cls, path):
#         if os.path.exists(path):
#             if os.path.isdir(path):
#                 return True
#         return False
#
#     @classmethod
#     def create(cls, path):
#         if cls.is_one(path) is True:
#             error('The data folder already exists therefore it cannot be created -> {0}'.format(path))
#         os.mkdir(path)
#         return cls(path)
#
#     def get_last_version(self):
#         last_data_version = -1
#         for data_version in self.get_versions():
#             last_data_index = last_data_version.get_index() if isinstance(last_data_version, Version) else -1
#             if data_version.get_index() > last_data_index:
#                 last_data_version = data_version
#         if isinstance(last_data_version, Version):
#             return last_data_version
#         return None
#
#     def get_files(self):
#         directories = list()
#         for directory in listdir(self.path):
#             path = join_path(self.path, directory)
#             if directory != Version.__class__.__name__.lower():
#                 if directory != VersionInfo.name:
#                     directories.append(path)
#         return directories
#
#     def create_version(self):
#         return Version.create(self)
#
#     def empty_folder(self):
#         for path in self.get_files():
#             os.remove(path)
#
#     def get_versions(self):
#         return Version.get_all(self)
#
#     def import_(self):
#         error('Import not implemented for this data.', prefix=self.__class__.__name__)
#
#     def export(self):
#         error('Export not implemented for this data.', prefix=self.__class__.__name__)
#
#     def get_type(self):
#         return split_path(self.path)[-1]
#
#
# class Version(Folder):
#
#     @classmethod
#     def create(cls, data):
#         last_version = data.get_last_version()
#         index = 0
#         if last_version is not None:
#             index = last_version.get_index() + 1
#
#         version_path = join_path(data.get_old_path(), str(index))
#         os.mkdir(version_path)
#
#         version = cls(version_path)
#
#         for path in data.get_files():
#             copy(path, version.get_path())
#
#         VersionInfo.create(version_path)
#         return version
#
#     @classmethod
#     def is_one(cls, path):
#         if os.path.exists(path):
#             if os.path.isdir(path):
#                 if split_path(path)[-1].isdigit():
#                     return True
#         return False
#
#     @classmethod
#     def get_all(cls, data):
#         data_versions = list()
#         for directory in listdir(data.get_path()):
#             if directory.isdigit():
#                 path = join_path(data.get_path(), directory)
#                 if Version.is_one(path):
#                     data_versions.append(Version(path))
#         return data_versions
#
#     def get_index(self):
#         split = split_path(self.path)
#         return int(split[-1])
#
#     def get_data_type_str(self):
#         split = split_path(self.path)
#         return int(split[-2])
#
#     def get_files(self):
#         paths = list()
#         for directory in listdir(self.path):
#             paths.append(join_path(self.path, directory))
#         return paths
#
#
# class VersionInfo(File):
#     name = 'info.json'
#
#     def get_dict(self):
#         with open(self.path) as f:
#             content = json.load(f)
#         return content
#
#     def get_user(self):
#         return self.get_dict()['user']
#
#     def get_creation_date(self):
#         return self.get_dict()['creation_date']
#
#     @classmethod
#     def create(cls, directory):
#         content = {'user': getpass.getuser(), 'creation_date': time.time()}
#         info_path = join_path(directory, cls.name)
#         if not os.path.exists(info_path):
#             with open(info_path, 'w') as f:
#                 json.dump(content, f)
#         return cls(info_path)
#
#     @classmethod
#     def is_one(cls, path):
#         if os.path.exists(path):
#             if os.path.isfile(path):
#                 if split_path(path)[-1] == cls.name:
#                     return True
#         return False


def f_msg(msg, prefix, suffix, new_line_after):
    s = ''

    if prefix != '':
        s += '{0} : '.format(prefix)

    s += str(msg)

    if suffix != '':
        s += ' / {0}'.format(suffix)

    if new_line_after:
        s += '\n'

    return s


def warning(msg='', prefix='', suffix='', new_line_after=False):
    cmds.warning(f_msg(msg, prefix, suffix, new_line_after))


def error(msg='', prefix='', suffix='', new_line_after=False):
    cmds.error(f_msg(msg, prefix, suffix, new_line_after))


def info(msg='', prefix='', suffix='', new_line_after=False):
    sys.stdout.write('{0}\n'.format(f_msg(msg, prefix, suffix, new_line_after)))


def get_widget(object_name, type_):
    pointer = omui.MQtUtil.findControl(object_name)
    return wrapInstance(long(pointer), type_)


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


def listdir(root, full=False):
    result = list()
    if os.path.isdir(root):
        try:
            paths = os.listdir(root)
            if full is False:
                result = paths
            else:
                for path in paths:
                    result.append(join_path(root, path))
        except WindowsError:
            pass
    result.sort()
    return result


def delete_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


def ask_build_window(details=''):
    mel.eval('closeNodeEditorEd nodeEditorPanel1NodeEditorEd;')
    message_box = QtWidgets.QMessageBox(get_widget('MayaWindow', QtWidgets.QWidget))
    message_box.setWindowTitle('Build')
    message_box.setText('Do you want to proceed?\n\n{0}'.format(details))
    message_box.addButton('Build', QtWidgets.QMessageBox.ButtonRole.YesRole)
    message_box.addButton('Cancel', QtWidgets.QMessageBox.ButtonRole.NoRole)
    message_box.buttons()[1].setFocus()
    button_pressed = message_box.exec_()

    if button_pressed == 0:
        return True

    return False


def build():
    Workspace.get_current().build()


def ask_build():
    if ask_build_window():
        if mel.eval('saveChanges("");'):
            build()
            return True

    warning('Build canceled.')
    return False


def setup_new_scene():
    cmds.file(new=True, force=True)


class Workspace(workspace_loader.Workspace):

    def build(self):
        info('Build {0}'.format(self.get_path()))

    def get_sub_folder_path(self, sub_folder):
        path = '{0}/data'.format(self.get_path(), sub_folder)
        if os.path.exists(path) is False:
            os.mkdir(path)
        return path

    def get_data_folder(self):
        return DataFolder.from_workspace(self)


class DataFolder(workspace_loader.Path):
    folder_name = 'data'

    @classmethod
    def from_workspace(cls, workspace):
        path = join_path(workspace.get_path(), cls.folder_name)
        if os.path.exists(path) is False:
            os.mkdir(path)
        return cls(path)

    def get_data(self):
        return Data.get_all_from_data_folder(self)


class Data(workspace_loader.Path):
    subclasses = list()

    @classmethod
    def is_one(cls, path):
        if os.path.isdir(path):
            if split_path(path)[-1] == cls.get_underscored_class_name():
                return True

    @classmethod
    def create(cls, path):
        if os.path.isdir(path):
            path = join_path(path, cls.get_underscored_class_name())
            if not os.path.exists(path):
                os.mkdir(path)
            return cls(path)
        return None

    @classmethod
    def get_all_from_data_folder(cls, data_folder):
        data = list()
        sub_classes = {class_.get_underscored_class_name(): class_ for class_ in cls.subclasses}
        for item in listdir(data_folder.get_path()):
            full_path = join_path(data_folder.get_path(), item)
            data_class = cls

            for name, class_ in sub_classes.items():
                if item == name:
                    data_class = class_

            command = 'if {0}.is_one(\'{1}\'): data.append({0}(\'{1}\'))'.format(data_class.__name__, full_path)
            exec command
        return data

    @classmethod
    def get_underscored_class_name(cls):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @classmethod
    def from_current_workspace(cls):
        workspace = Workspace.get_current()

        if workspace is None:
            warning('Unable to find the current workspace. Skip...', prefix=cls.__name__)
            return

        path = join_path(workspace.get_data_path(), cls.get_underscored_class_name())
        if os.path.exists(path):
            return cls(path)

        return None

    def import_(self):
        pass

    def export(self):
        pass

    def create_version(self):
        return Version.create(self)

    def get_versions(self):
        return Version.get_all(self)

    def get_latest_version(self):
        versions = self.get_versions()
        print versions
        if versions:
            return versions[-1]
        return None

    def get_children(self):
        children = list()
        for item in listdir(self.get_path()):
            path = join_path(self.get_path(), item)
            if item != VersionFolder.folder_name:
                children.append(path)
        return children


class ExportHelper(object):

    def __init__(self, data):
        self.__data = data

    def __enter__(self):
        self.__data.wipe_out_root()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__data.create_version()


class VersionFolder(workspace_loader.Path):
    folder_name = 'versions'

    @classmethod
    def retrieve(cls, data):
        versions_path = join_path(data.get_path(), cls.folder_name)
        if not os.path.exists(versions_path):
            os.mkdir(versions_path)
        return cls(versions_path)


class Version(workspace_loader.Path):

    @classmethod
    def create(cls, data):
        last_version = data.get_latest_version()
        print last_version
        index = 0
        if last_version is not None:
            index = last_version.get_index() + 1

        versions = VersionFolder.retrieve(data)
        version_path = join_path(versions.get_path(), str(index))
        os.mkdir(version_path)

        version = cls(version_path)

        for path in data.get_children():
            copy(path, version.get_path())

        # VersionInfo.create(version_path)
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
        versions = VersionFolder.retrieve(data)
        for item in listdir(versions.get_path()):
            if item.isdigit():
                path = join_path(versions.get_path(), item)
                if Version.is_one(path):
                    data_versions.append(Version(path))
        return data_versions

    def get_index(self):
        split = split_path(self.get_path())
        return int(split[-1])

    def get_data_type_str(self):
        split = split_path(self.get_path())
        return int(split[-2])

    def get_children(self):
        return listdir(self.get_path(), full=True)


class Builder(Data):

    def __init__(self, path):
        super(Builder, self).__init__(path)
        file_name = '{0}.py'.format(self.get_underscored_class_name())
        self.file = join_path(self.get_path(), file_name)

    def exec_(self):
        if not os.path.exists(self.file):
            pass

        # if self.has_changed():
        #     self.create_version()

        execfile(self.file)

    def open_file(self):
        webbrowser.open(self.file)

    def read(self):
        with open(self.file, 'r') as f:
            return f.read()

    def write(self, content=''):
        with open(self.file, 'w') as f:
            f.write(content)

    # @classmethod
    # def create(cls, path):
    #     builder = super(Builder, cls).create(path)
    #
    #     if builder is not None:
    #         builder.write()

    # def replace_by(self, builder):
    #     with open(builder.get_directory() + '/builder.py', 'r') as f:
    #         builder_content = f.read()
    #
    #     with open(self.directory + '/builder.py', 'w') as f:
    #         f.write(builder_content)
    #     self.imported_msg()
    #     self.make_copy()
    #
    # def has_changed(self):
    #     latest_builder_version = self.get_latest_version_path()
    #     if latest_builder_version:
    #         lastest_builder = latest_builder_version + '/builder.py'
    #         if not os.path.exists(lastest_builder):
    #             return True
    #         with open(self.directory + '/builder.py', 'r') as f:
    #             current_builder_content = f.read()
    #
    #         with open(lastest_builder, 'r') as f:
    #             latest_builder_version_content = f.read()
    #
    #         if current_builder_content == latest_builder_version_content:
    #             return False
    #
    #     return True


class Build(object):

    def __init__(self):
        self.steps = list()

    def __iter__(self):
        return iter(self.steps)

    def append_step(self, callable_):
        if not isinstance(callable_, types.FunctionType) and not isinstance(callable_, types.MethodType):
            warning('The given item is not of type \'function\' or \'instancemethod\'. Got -> \'{0}\' of type -> \'{1}\'. Skipping...'.format(callable_, type(callable_)), prefix=self.__class__.__name__)
            return
        self.steps.append(callable_)

    def run(self, clear_script_editor=True, new_scene=True):
        if clear_script_editor is True:
            try:
                cmds.cmdScrollFieldReporter(mel.eval('string $tmp = $gCommandReporter;'), e=True, clear=True)
            except:
                pass

        if new_scene is True:
            self.steps.insert(0, setup_new_scene)

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

# #################################################
#
# # def exec_():
# #     result = ask_build_rig(title='Build And Pre-Publish')
# #
# #     if result == kSaveBuild:
# #         o2o.globals.LOADER.save_current_scene()
# #
# #     if result >= kBuild:
# #         SidePublish().run(rebuild=True)
# #
# #     if result == kCancel:
# #         warning('Importation/Build canceled.')
#
# def show_data_ui():
#     start = time.time()
#     DataUI.show_dialog()
#     delta = time.time() - start
#     info('Import Data From Other opened in {0} sec.'.format(delta))
#
#
# class MetaAsset(object):
#
#     def __init__(self, path):
#         if not self.is_one(path):
#             raise
#         self.path = path
#         self.widget = None
#
#     def set_widget(self, widget):
#         self.widget = widget
#
#     def get_widget(self):
#         return self.widget
#
#     def get_name(self):
#         return split_path(self.get_path())[-1]
#
#     def is_one(self, *args, **kwargs):
#         return False
#
#     def get_path(self):
#         return self.path
#
#     def get_comment(self):
#         comment_directory = '{0}/comment.txt'.format(self.get_path())
#         if os.path.exists(comment_directory):
#             with open(comment_directory, 'r') as f:
#                 content = f.read()
#             return content.strip()
#
#         return ''
#
#     def is_executable(self):
#         return False
#
#     def set_comment(self, string):
#         comment_directory = '{0}/comment.txt'.format(self.get_path())
#         if string == '':
#             if os.path.exists(comment_directory):
#                 os.remove(comment_directory)
#             return
#
#         with open(comment_directory, 'w') as f:
#             f.write(string.strip())
#
#     def get_info(self):
#         file_ = '{0}/version_info.json'.format(self.get_path())
#         user, date = '', ''
#         if os.path.exists(file_):
#             with open(file_, 'r') as f:
#                 content = json.load(f)
#             for key, value in content.items():
#                 if key == 'user':
#                     user = value
#                 elif key == 'date':
#                     date = datetime.datetime.fromtimestamp(value).strftime('%d/%m/%y %H:%M:%S')
#         return user, date
#
#     def get_title(self):
#         user, date = self.get_info()
#         return self.get_name(), user, date, self.get_comment()
#
#
# class SidePublish(object):
#     """
#     root = '{0}/work/rigLibrary'.format(const.get_project_root())
#
#     publish_file_directory_pattern = '{0}/library/assets/<asset_type>/<asset_name>/rig/rig/ma'.format(const.get_project_root())
#     publish_file_name_prefix_pattern = 'idx_<asset_name>_rig-rig_base_v'
#     publish_file_name_suffix_pattern = '.ma'
#
#     rig_data_root = '{0}/work/assets/<asset_type>/<asset_name>/rig/rig/<user>/maya/data'.format(const.get_project_root())
#
#     data_types_to_mind = {
#         data.GuideData.grp_name: data.GuideData,
#         data.CtrlsData.grp_name: data.CtrlsData,
#         data.SkinLayersData.grp_name: data.SkinLayersData,
#         data.BuilderData.grp_name: data.BuilderData,
#         data.TmpDagsData.grp_name: data.TmpDagsData,
#         data.PickerData.grp_name: data.PickerData,
#         data.AttributeMapData.grp_name: data.AttributeMapData,
#         data.DeleteFacesData.grp_name: data.DeleteFacesData,
#         data.FacialGuideData.grp_name: data.FacialGuideData,
#         data.BcsData.grp_name: data.BcsData,
#         data.EyesSurfacesData.grp_name: data.EyesSurfacesData,
#         'zv_parent': data.ZvParentData,
#         data.HardSkinGuideData.grp_name: data.HardSkinGuideData,
#         data.HiddenFacesData.grp_name: data.HiddenFacesData,
#         data.SkinMapData.grp_name: data.SkinMapData
#     }
#     """
#
#     def __init__(self):
#         self.asset_name, self.asset_type, _ = v.Misc.get_asset_info()
#
#         self.publish_file_directory_pattern = self.publish_file_directory_pattern.replace('<asset_name>', self.asset_name).replace('<asset_type>', self.asset_type.lower())
#         self.publish_file_name_prefix_pattern = self.publish_file_name_prefix_pattern.replace('<asset_name>', self.asset_name)
#
#         self.asset_folder = ''
#         self.data_folder = ''
#         self.setup_folder()
#
#     def run(self, rebuild=False):
#         if rebuild:
#             BuilderData.from_asset().exec_()
#
#         # Save work file
#         work_file = self.ask_to_save_file()
#         if not work_file:
#             raise ValueError('You must save your scene to proceed!')
#         version_folder = self.setup_version_folder()
#         self.copy_file_to(work_file, version_folder, name='work.ma')
#
#         # Save lock file
#         steps.LockRig().run()
#         lock_file = self.ask_to_save_file(force_save_as=True)
#         if not lock_file:
#             raise ValueError('You must save your scene to proceed!')
#         self.copy_file_to(lock_file, version_folder, name='lock.ma')
#
#         # Save latest data
#         self.data_folder = version_folder + '/data'
#         if not os.path.exists(self.data_folder):
#             os.mkdir(self.data_folder)
#         self.copy_latest_data()
#         v.info('Published!')
#
#         # Save info
#         with open('{0}/version_info.json'.format(version_folder), 'w') as f:
#             json.dump({'user': getpass.getuser(), 'date': time.time()}, f)
#
#     def setup_folder(self):
#         if not os.path.exists(self.root):
#             raise ValueError('The root path does not exist!')
#
#         type_folder = self.root + '/' + self.asset_type
#         if not os.path.exists(type_folder):
#             os.mkdir(type_folder)
#
#         self.asset_folder = type_folder + '/' + self.asset_name
#         if not os.path.exists(self.asset_folder):
#             os.mkdir(self.asset_folder)
#
#     @staticmethod
#     def ask_to_save_file(force_save_as=False):
#         if not cmds.file(q=True, sn=True) or force_save_as:
#             mel.eval('SaveSceneAs;')
#             if not cmds.file(q=True, sn=True):
#                 return ''
#         return cmds.file(save=True)
#
#     def setup_version_folder(self):
#         # Search last version
#         new_index = 1
#         if os.path.exists(self.publish_file_directory_pattern):
#             indices = list()
#             for item in os.listdir(self.publish_file_directory_pattern):
#                 item_path = self.publish_file_directory_pattern + '/' + item
#                 if os.path.isfile(item_path):
#                     if item.startswith(self.publish_file_name_prefix_pattern) and item.endswith(self.publish_file_name_suffix_pattern):
#                         index_str = item.replace(self.publish_file_name_prefix_pattern, '').replace(self.publish_file_name_suffix_pattern, '')
#                         indices.append(int(index_str))
#             if indices:
#                 new_index = max(indices) + 1
#
#         # Create a new version
#         new_version_folder = self.asset_folder + '/' + '{:04d}'.format(new_index)
#         if not os.path.exists(new_version_folder):
#             os.mkdir(new_version_folder)
#         else:
#             self.clean_up_folder(new_version_folder)
#
#         return new_version_folder
#
#     @staticmethod
#     def copy_file_to(file_path, directory, name=''):
#         if not os.path.exists(file_path) or not os.path.exists(directory):
#             raise ValueError('The given file path or directory does not exist. Given -> {0}, {1}'.format(file_path, directory))
#
#         file_name = file_path.split('/')[-1] if not name else name
#         copied_file_path = directory + '/' + file_name
#
#         with open(file_path, 'r') as f:
#             content = f.read()
#
#         with open(copied_file_path, 'w') as f:
#             f.write(content)
#
#         return copied_file_path
#
#     @staticmethod
#     def clean_up_folder(directory):
#         for item in os.listdir(directory):
#             item_path = directory + '/' + item
#             if os.path.isfile(item_path):
#                 os.remove(item_path)
#             elif os.path.isdir(item_path):
#                 shutil.rmtree(item_path)
#
#     def copy_latest_data(self):
#         source_asset_data_folder = self.rig_data_root.replace('<asset_type>', self.asset_type).replace('<asset_name>', self.asset_name).replace('<user>', getpass.getuser())  # + '/' + self.asset_type + '/' + self.asset_name
#         source_data_paths = list()
#         for item in os.listdir(source_asset_data_folder):
#             if item in self.data_types_to_mind:
#                 source_data_path = source_asset_data_folder + '/' + item
#                 source_data_old_path = source_data_path + '/old'
#                 if os.path.exists(source_data_old_path):
#                     version_indices = list()
#                     for version_index_str in os.listdir(source_data_old_path):
#                         try:
#                             version_indices.append(int(version_index_str))
#                         except:
#                             pass
#                     if version_indices:
#                         last_version_index = max(version_indices)
#                         last_version_index_str = '{:04d}'.format(last_version_index)
#                         last_version_path = source_data_old_path + '/' + last_version_index_str
#                         source_data_paths.append(last_version_path)
#
#         for source_data_path in source_data_paths:
#             source_data_path_split = source_data_path.split('/')
#             source_data_type = source_data_path_split[-3]
#             source_data_version = source_data_path_split[-1]
#
#             destination_data_type_folder = self.data_folder + '/' + source_data_type
#             if not os.path.exists(destination_data_type_folder):
#                 os.mkdir(destination_data_type_folder)
#
#             destination_data_version_folder = destination_data_type_folder + '/' + source_data_version
#             if not os.path.exists(destination_data_version_folder):
#                 os.mkdir(destination_data_version_folder)
#
#             for item in os.listdir(source_data_path):
#                 item_path = source_data_path + '/' + item
#                 if os.path.isfile(item_path):
#                     self.copy_file_to(item_path, destination_data_version_folder)
#
#
# # class AssetType(MetaAsset):
# #     authorized_types = ('Character', 'Prop')
# #
# #     @classmethod
# #     def is_one(cls, path):
# #         if data_dir in path:
# #             if os.path.isdir(path):
# #                 if path.split('/')[-1] in cls.authorized_types:
# #                     return True
# #         return False
# #
# #     @classmethod
# #     def get_all(cls):
# #         asset_types = list()
# #         for child in listdir(data_dir, full_path=True):
# #             if cls.is_one(child):
# #                 asset_types.append(cls(child))
# #         return asset_types
# #
# #     def get_assets(self):
# #         assets = list()
# #         for child in listdir(self.path, full_path=True):
# #             if AssetName.is_one(child):
# #                 assets.append(AssetName(child))
# #         return assets
# #
# #     def is_executable(self):
# #         return False
# #
# #     def exec_(self):
# #         return
#
#
# # class AssetName(MetaAsset):
# #
# #     @classmethod
# #     def is_one(cls, path):
# #         if data_dir in path:
# #             if os.path.isdir(path):
# #                 if path.split('/')[-1] in [item.code for item in o2o.globals.LOADER.data.assets]:
# #                     return True
# #         return False
# #
# #     def has_versions(self):
# #         path = self.get_path()
# #         if os.path.isdir(path):
# #             for child in listdir(path):
# #                 full_path = join_path(path, child)
# #                 if os.path.isdir(full_path):
# #                     if child.isdigit():
# #                         return True
# #         return False
# #
# #     def get_lib_path(self):
# #         return '{0}/library/assets/{1}/{2}/rig/rig/ma'.format(const.get_project_root(), self.get_type().get_name().lower(), self.get_name())
# #
# #     def get_lib_file_suffix(self):
# #         return '{0}_{1}_rig-rig_base_v'.format(const.get_prod_name(), self.get_name())
# #
# #     """
# #     def get_versions(self):
# #         entity = o2o.globals.LOADER.data.get_asset_by_code(self.get_name())
# #         task = entity.get_task_by_name("rig")
# #         versions = list()
# #         for publish in task.publishes:
# #             if AssetVersion.is_one(self, publish.version):
# #                 versions.append(AssetVersion(self, publish.version))
# #         return versions
# #     """
# #
# #     def get_versions(self):
# #         lib_path = self.get_lib_path()
# #
# #         versions = list()
# #         if os.path.exists(lib_path):
# #             for child in listdir(lib_path, full_path=False):
# #                 full_path = join_path(lib_path, child)
# #
# #                 if not os.path.isfile(full_path):
# #                     continue
# #                 if not child.endswith('.ma'):
# #                     continue
# #                 if not child.startswith(self.get_lib_file_suffix()):
# #                     continue
# #
# #                 index_str = child.replace(self.get_lib_file_suffix(), '').replace('.ma', '')
# #
# #                 if not index_str.isdigit():
# #                     continue
# #
# #                 index = int(index_str)
# #
# #                 if not AssetVersion.is_one(self, index):
# #                     continue
# #
# #                 versions.append(AssetVersion(self, index))
# #         return versions
# #
# #     def is_executable(self):
# #         return True
# #
# #     def get_type(self):
# #         asset_type = '/'.join(self.path.split('/')[:-1])
# #         if AssetType.is_one(asset_type):
# #             return AssetType(asset_type)
# #         return None
# #
# #     def get_last_version(self):
# #         versions = self.get_versions()
# #         if versions:
# #             last = None
# #             for version in versions:
# #                 if version.exists():
# #                     last = version
# #             return last
# #         return None
# #
# #     def exec_(self):
# #         last_version = self.get_last_version()
# #         if not last_version:
# #             v.warning('No last version found for {0}.'.format(self.get_name()))
# #             return
# #         v.info('Building: {0} {1}.'.format(self.get_name(), last_version.get_name()))
# #         last_version.exec_()
#
#
# class AssetVersion(MetaAsset):
#
#     def __init__(self, asset, index):
#         if not self.is_one(asset, index):
#             raise ValueError
#         self.asset = asset
#         self.index = index
#         self.widget = None
#
#     @classmethod
#     def is_one(cls, asset, index):
#         if isinstance(asset, AssetName) and isinstance(index, int):
#             return True
#         return False
#
#     def exists(self):
#         return os.path.isdir(self.get_path())
#
#     def get_path(self):
#         return join_path(self.asset.get_path(), self.get_formatted_version_index())
#
#     def get_formatted_version_index(self):
#         return "{:04d}".format(self.index)
#
#     def get_data(self):
#         if self.exists():
#             data_ = list()
#             for child in listdir(join_path(self.get_path(), 'data'), full_path=True):
#                 if AssetData.is_one(child):
#                     data_.append(AssetData(child))
#             return data_
#         return list()
#
#     def get_version_title(self):
#         string = self.get_formatted_version_index()
#         if not self.exists():
#             string += ' (no data published)'
#         return string
#
#     def get_title(self):
#         asset_name, date, from_, comment = super(AssetVersion, self).get_title()
#         return self.get_version_title(), date, from_, comment
#
#     def is_executable(self):
#         if self.exists():
#             return True
#         return False
#
#     def get_data_dir(self):
#         data_path = join_path(self.get_path(), 'data')
#         if os.path.isdir(data_path):
#             return data_path
#         return ''
#
#     def exec_(self):
#         result = ask_build_rig('From published version: {0}'.format(int(self.get_name())))
#
#         if result == kSaveBuild:
#             o2o.globals.LOADER.save_current_scene()
#         if result >= kBuild:
#             for data_ in self.get_data():
#                 data_.get_class().from_asset().make_copy_in_workspace(data_.get_path())
#             BuilderData.from_asset().exec_()
#         if result == kCancel:
#             warning('Importation/Build canceled.')
#
#     def set_comment(self, string):
#         if self.exists():
#             super(self.__class__, self).set_comment(string)
#         else:
#             warning('Unable to comment not linked version.')
#
#
# class AssetData(MetaAsset):
#     """
#     data_types = SidePublish.data_types_to_mind
#     """
#
#     @classmethod
#     def is_one(cls, path):
#         if data_dir in path:
#             if os.path.isdir(path):
#                 if path.split('/')[-1] in cls.data_types.keys():
#                     return True
#         return False
#
#     def get_class(self):
#         return self.data_types[self.get_data_type_name()]
#
#     def is_executable(self):
#         return True
#
#     def exec_(self):
#         data_type = self.get_data_type_name()
#         asset_name = self.get_asset().get_name()
#         asset_type = self.get_asset().get_type().get_name()
#         data_path = self.get_path()
#         if data_type == 'builder':
#             BuilderData.from_asset().replace_by(self.data_types[data_type](data_path, asset_name=asset_name, asset_type=asset_type))
#         else:
#             self.data_types[data_type](data_path, asset_name=asset_name, asset_type=asset_type).import_()
#
#     def get_asset(self):
#         asset_path = '/'.join(self.path.split('/')[:-3])
#         if AssetName.is_one(asset_path):
#             return AssetName(asset_path)
#         return None
#
#     def get_path(self):
#         root = super(AssetData, self).get_path()
#         for path in listdir(root):
#             full_path = join_path(root, path)
#             if os.path.isdir(full_path):
#                 if path.isdigit():
#                     return full_path
#         return ''
#
#     def get_data_type_name(self):
#         return self.get_path().split('/')[-2]
#
#     def get_title(self):
#         asset_name, date, from_, comment = super(self.__class__, self).get_title()
#         return self.get_data_type_name(), date, from_, comment
#
#
# class DataUI(QtWidgets.QDialog):
#     """
#     authorized_asset_types = ('Character', 'Prop')
#     ignored_asset_names = ('test',)
#
#     data_types = SidePublish.data_types_to_mind
#     """
#
#     def __init__(self):
#         super(self.__class__, self).__init__(get_widget('MayaWindow', QtWidgets.QWidget))
#
#         # Refresh timer
#         self.timer = time.time()
#
#         # Dialog
#         self.setWindowTitle('Import Data From Other')
#         self.setObjectName(self.__class__.__name__)
#         self.setMinimumWidth(500)
#         self.setMinimumHeight(700)
#
#         # Remove useless flags
#         if cmds.about(ntOS=True):
#             self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
#         elif cmds.about(macOS=True):
#             self.setWindowFlags(QtCore.Qt.Tool)
#
#         # Main list
#         self.data_tree = QtWidgets.QTreeWidget()
#         self.data_tree.setHeaderLabels(['asset', 'from', 'date', 'comment'])
#         self.data_tree.setColumnWidth(0, 200)
#         self.data_tree.doubleClicked.connect(self.double_click)
#         self.refresh_tree()
#
#         # Layout
#         main_lay = QtWidgets.QVBoxLayout(self)
#         main_lay.addWidget(self.data_tree)
#
#         # Actions
#         self.set_comment_action = QtWidgets.QAction('Comment', self)
#         self.set_comment_action.triggered.connect(self.set_comment)
#
#         # Context Menu
#         self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
#         self.customContextMenuRequested.connect(self.show_context_menu)
#
#     @classmethod
#     def show_dialog(cls):
#         for child in get_widget('MayaWindow', QtWidgets.QWidget).children():
#             if type(child).__name__ == cls.__name__:
#                 child.deleteLater()
#
#         inst = cls()
#         inst.show()
#
#         return inst
#
#     def show_context_menu(self, point):
#         menu = QtWidgets.QMenu(self)
#         menu.addAction(self.set_comment_action)
#         menu.addSeparator()
#         menu.exec_(self.mapToGlobal(point))
#
#     def refresh_tree(self):
#         # Clear tree
#         self.data_tree.clearSelection()
#         self.data_tree.clear()
#
#         asset_types = list()
#         for asset_type in AssetType.get_all():
#             widget = QtWidgets.QTreeWidgetItem(asset_type.get_title())
#             widget.setData(0, QtCore.Qt.UserRole, asset_type)
#             self.data_tree.addTopLevelItem(widget)
#             asset_type.set_widget(widget)
#             asset_types.append(asset_type)
#
#         asset_names = list()
#         for asset_type in asset_types:
#             for asset_name in asset_type.get_assets():
#                 if asset_name.has_versions():
#                     widget = QtWidgets.QTreeWidgetItem(asset_name.get_title())
#                     widget.setData(0, QtCore.Qt.UserRole, asset_name)
#                     asset_type.get_widget().addChild(widget)
#                     asset_name.set_widget(widget)
#                     asset_names.append(asset_name)
#
#         asset_versions = list()
#         for asset_name in asset_names:
#             for asset_version in asset_name.get_versions():
#                 widget = QtWidgets.QTreeWidgetItem(asset_version.get_title())
#                 widget.setData(0, QtCore.Qt.UserRole, asset_version)
#                 asset_name.get_widget().addChild(widget)
#                 asset_version.set_widget(widget)
#                 asset_versions.append(asset_version)
#
#         asset_datas = list()
#         for asset_version in asset_versions:
#             for asset_data in asset_version.get_data():
#                 widget = QtWidgets.QTreeWidgetItem(asset_data.get_title())
#                 widget.setData(0, QtCore.Qt.UserRole, asset_data)
#                 asset_version.get_widget().addChild(widget)
#                 asset_data.set_widget(widget)
#                 asset_datas.append(asset_data)
#
#     def double_click(self):
#         selected_items = self.data_tree.selectedItems()
#
#         for item in selected_items:
#             data_ = item.data(0, QtCore.Qt.UserRole)
#             if data_.is_executable():
#                 data_.exec_()
#             else:
#                 item.setExpanded(not item.isExpanded())
#
#     def set_comment(self):
#         selected_items = self.data_tree.selectedItems()
#         if selected_items:
#             data_ = selected_items[0].data(0, QtCore.Qt.UserRole)
#             string = QtWidgets.QInputDialog.getText(self, 'Edit Comment', 'Comment:', text=data_.get_comment())[0]
#             data_.set_comment(string)
#             self.refresh_tree()
#
# # class Builder(object):
# #
# #     def __init__(self):
# #         self.queue = list()
# #         self.data = dict()
# #         # self.progress_bar = o2o_pyqt.ProgressDialog(name='Builder')
# #         # self.progress_bar.auto_close = True
# #         # self.progress_bar.progress.auto_refresh = True
# #
# #     def add_step(self, input_):
# #         step = None
# #         if isinstance(input_, str) or isinstance(input_, unicode):
# #             try:
# #                 exec 'step = steps.{0}(d=self.data)'.format(input_)
# #             except:
# #                 pass
# #         elif isinstance(input_, types.FunctionType):
# #             step = input_
# #         else:
# #             raise ValueError('Unrecognized input.')
# #
# #         self.queue.append(step)
# #
# #     def run(self):
# #         try:
# #             reporter = mel.eval('string $tmp = $gCommandReporter;')
# #             cmds.cmdScrollFieldReporter(reporter, e=True, clear=True)
# #         except RuntimeError:
# #             pass
# #
# #         start = time.time()
# #         cmds.warning('Rig build starts.')
# #
# #         with open(stop_file, 'w') as f:
# #             f.write('plop')
# #
# #         # Run steps
# #         # self.progress_bar.progress.max = len(self.queue)
# #         # self.progress_bar.run()
# #         for step in self.queue:
# #             if not os.path.exists(stop_file):
# #                 v.error('Build stops!')
# #             if isinstance(step, steps.Step):
# #                 # self.progress_bar.progress.text = step.__class__.__name__
# #                 v.info('{0} {1}: starts {0}'.format('-' * 10, step.__class__.__name__))
# #                 step.run()
# #                 v.info('{0} {1}: ends {0}\n'.format('-' * 10, step.__class__.__name__))
# #             elif isinstance(step, types.FunctionType):
# #                 # self.progress_bar.progress.text = step.__name__
# #                 v.info('{0} {1}: starts {0}'.format('-' * 10, step.__name__))
# #                 try:
# #                     step(self.data)
# #                 except:
# #                     step()
# #                 v.info('{0} {1}: ends {0}\n'.format('-' * 10, step.__name__))
# #             else:
# #                 cmds.warning('Unable to run this step -> {0}'.format(step))
# #             # self.progress_bar.progress.increment()
# #
# #         delta = time.time() - start
# #         cmds.warning('Asset built in {0} sec.'.format(delta))
# #
# #     @staticmethod
# #     def speed_test():
# #         start = time.time()
# #
# #         frame_count = 120
# #         for i in range(1, frame_count + 1):
# #             cmds.currentTime(i)
# #
# #         delta = time.time() - start
# #         return int(frame_count / delta)
#
# #
# # def setup_top_main():
# #     root_path = '{0}/work/rigResources/top_main/'.format(const.get_project_root())
# #     guide_path = '{0}/guide'.format(root_path)
# #     builder_path = '{0}/builder'.format(root_path)
# #     ctrls_path = '{0}/ctrls'.format(root_path)
# #     zv_path = '{0}/zv_parent'.format(root_path)
# #
# #     guide = data.GuideData.from_asset()
# #     guide.make_copy_in_workspace(guide_path)
# #
# #     ctrls = data.CtrlsData.from_asset()
# #     ctrls.make_copy_in_workspace(ctrls_path)
# #
# #     zv = data.ZvParentData.from_asset()
# #     zv.make_copy_in_workspace(zv_path)
# #
# #     builder = data.BuilderData.from_asset()
# #     builder.make_copy_in_workspace(builder_path)
# #     builder.exec_()
# #
# #     meshes = r.get_meshes()
# #     result = cmds.exactWorldBoundingBox(meshes)
# #     p1, p2 = result[:3], result[3:]
# #     mid_point = [(v1 + v2) / 2 for v1, v2 in zip(p1, p2)]
# #
# #     # Place cog
# #     cog = 'cog_C0_root'
# #     if cmds.objExists(cog):
# #         cmds.xform(cog, translation=mid_point, absolute=True)
# #         guide.export()
# #
# #     # Scale ctrls
# #     base_distance = 5.71842046409
# #     current_distance = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
# #     ratio = current_distance / base_distance
# #
# #     ctrls_ = controller.Ctrl.get_all()
# #     for ctrl in ctrls_:
# #         ctrl.scale_shapes(v.axes, ratio)
# #
# #     if ctrls_:
# #         ctrls.export()
# #
# #     builder.exec_()
# #
# #     # side_publish.SidePublish().run(rebuild=False)
