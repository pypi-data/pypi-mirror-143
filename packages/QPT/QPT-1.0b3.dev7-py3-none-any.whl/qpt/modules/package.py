# Author: Acer Zhang
# Datetime: 2021/5/26 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import os
import shutil

from qpt.version import version as qpt_version
from qpt.modules.base import SubModule, SubModuleOpt, TOP_LEVEL_REDUCE, LOW_LEVEL, GENERAL_LEVEL
from qpt.kernel.qos import FileSerialize, ArgManager
from qpt.kernel.qlog import Logging
from qpt.kernel.qcode import PythonPackages
from qpt.memory import QPT_MEMORY

# 第三方库部署方式
FLAG_FILE_SERIALIZE = "[FLAG-FileSerialize]"
LOCAL_DOWNLOAD_DEPLOY_MODE = "为用户准备Whl包，首次启动时会自动安装，即使这样也可能会有兼容性问题"
LOCAL_INSTALL_DEPLOY_MODE = "[不推荐]预编译第三方库，首次启动无需安装但将额外消耗硬盘空间，可能会有兼容性问题并且只支持二进制包"
ONLINE_DEPLOY_MODE = "用户使用时在线安装Python第三方库"
DEFAULT_DEPLOY_MODE = LOCAL_DOWNLOAD_DEPLOY_MODE

# 第三方库下载版本
PACKAGE_FOR_PYTHON38_VERSION = "3.8"
DEFAULT_PACKAGE_FOR_PYTHON_VERSION = None  # None表示不设置


def set_default_deploy_mode(mode):
    """
    设置全局部署方式
    :param mode: 部署方式
    """
    global DEFAULT_DEPLOY_MODE
    DEFAULT_DEPLOY_MODE = mode


def set_default_package_for_python_version(version):
    """
    设置全局下载的Python包默认解释器版本号
    :param version: Python版本号
    """
    global DEFAULT_PACKAGE_FOR_PYTHON_VERSION
    DEFAULT_PACKAGE_FOR_PYTHON_VERSION = version


class DownloadWhlOpt(SubModuleOpt):
    def __init__(self,
                 package: str = "",
                 version: str = None,
                 no_dependent=False,
                 find_links: str = None,
                 python_version=DEFAULT_PACKAGE_FOR_PYTHON_VERSION,
                 opts: ArgManager = None):
        super().__init__()
        if opts is None:
            opts = ArgManager()
        self.package = package
        self.no_dependent = no_dependent
        self.find_links = find_links
        self.opts = opts
        self.version = version
        self.python_version = python_version

    def act(self) -> None:
        # 对固化的Requirement文件进行解冻
        if FLAG_FILE_SERIALIZE in self.package[:32]:
            self.opts += "-r " + FileSerialize.serialize2file(self.package.strip(FLAG_FILE_SERIALIZE))
            self.package = ""
        QPT_MEMORY.pip_tool.download_package(self.package,
                                             version=self.version,
                                             save_path=os.path.join(self.module_path,
                                                                    QPT_MEMORY.get_down_packages_relative_path),
                                             no_dependent=self.no_dependent,
                                             find_links=self.find_links,
                                             python_version=self.python_version,
                                             opts=self.opts)


class LocalInstallWhlOpt(SubModuleOpt):
    def __init__(self,
                 package: str = "",
                 version: str = None,
                 static_whl: bool = False,  # 控制是否从镜像源安装
                 no_dependent=False,
                 opts: ArgManager = None):
        super().__init__(disposable=True)
        if opts is None:
            opts = ArgManager()
        self.package = package
        self.static_whl = static_whl
        self.no_dependent = no_dependent
        self.opts = opts
        self.version = version

    def act(self) -> None:
        if FLAG_FILE_SERIALIZE in self.package[:32]:
            self.opts += "-r " + FileSerialize.serialize2file(self.package.strip(FLAG_FILE_SERIALIZE))
            self.package = ""
        self.opts += "--target " + self.module_site_package_path

        if self.static_whl:
            QPT_MEMORY.pip_tool.install_local_package(os.path.join(self.packages_path, os.path.basename(self.package)),
                                                      abs_package=True,
                                                      version=self.version,
                                                      whl_dir=os.path.join(self.module_path,
                                                                           QPT_MEMORY.get_down_packages_relative_path),
                                                      no_dependent=self.no_dependent,
                                                      opts=self.opts)
        else:
            QPT_MEMORY.pip_tool.install_local_package(self.package,
                                                      version=self.version,
                                                      whl_dir=os.path.join(self.module_path,
                                                                           QPT_MEMORY.get_down_packages_relative_path),
                                                      no_dependent=self.no_dependent,
                                                      opts=self.opts)


class OnlineInstallWhlOpt(SubModuleOpt):
    def __init__(self,
                 package: str = "",
                 version: str = None,
                 to_module_env_path=True,
                 to_python_env_version=DEFAULT_PACKAGE_FOR_PYTHON_VERSION,
                 no_dependent=False,
                 find_links: str = None,
                 opts: ArgManager = None):
        super().__init__(disposable=True)
        if opts is None:
            opts = ArgManager()
        self.package = package
        self.to_module_env = to_module_env_path
        self.no_dependent = no_dependent
        self.find_links = find_links
        self.opts = opts
        self.version = version
        self.to_python_env_version = to_python_env_version
        if to_python_env_version:
            assert to_module_env_path, "安装在当前环境则不需要设置Python版本号参数to_python_env_version。" \
                                       "若需要安装其它位置，请设置to_module_env_path参数使包安装在其它位置。"
            self.to_python_env_version = DEFAULT_PACKAGE_FOR_PYTHON_VERSION

    def act(self) -> None:
        if FLAG_FILE_SERIALIZE in self.package[:32]:
            self.opts += "-r " + FileSerialize.serialize2file(self.package.strip(FLAG_FILE_SERIALIZE))
            self.package = ""
        if self.to_module_env:
            self.opts += "--target " + self.module_site_package_path
            if self.to_python_env_version:
                self.opts += f"--python-version {self.to_python_env_version} --only-binary :all:"
        QPT_MEMORY.pip_tool.pip_package_shell(self.package,
                                              act="install",
                                              version=self.version,
                                              find_links=self.find_links,
                                              no_dependent=self.no_dependent,
                                              opts=self.opts)


class BatchInstallationOpt(SubModuleOpt):
    def __init__(self, path=None):
        super(BatchInstallationOpt, self).__init__(disposable=True)
        self.path = path

    def act(self) -> None:
        if self.path is None:
            self.path = os.path.join(self.module_path, QPT_MEMORY.get_down_packages_relative_path)

        # 模糊匹配
        ready_list = " ".join([k.lower() for k in PythonPackages.search_packages_dist_info()[0].keys()])
        whl_list = [whl for whl in os.listdir(self.path)
                    if whl.split("-")[0].lower() not in ready_list]
        Logging.info(f"需要补充的安装包数量为：{len(whl_list)}")
        for whl_name in whl_list:
            QPT_MEMORY.pip_tool.install_local_package(os.path.join(self.packages_path, whl_name),
                                                      abs_package=True,
                                                      no_dependent=True)


class CustomPackage(SubModule):
    def __init__(self,
                 package="",
                 version: str = None,
                 deploy_mode=None,
                 no_dependent=False,
                 find_links: str = None,
                 opts: ArgManager = None):
        super().__init__(name=None)
        if opts is None:
            opts = ArgManager()
        if deploy_mode is None:
            deploy_mode = DEFAULT_DEPLOY_MODE
        if deploy_mode == LOCAL_DOWNLOAD_DEPLOY_MODE:
            self.add_pack_opt(DownloadWhlOpt(package=package,
                                             version=version,
                                             no_dependent=no_dependent,
                                             find_links=find_links,
                                             opts=opts))
            self.add_unpack_opt(LocalInstallWhlOpt(package=package,
                                                   version=version,
                                                   no_dependent=no_dependent,
                                                   opts=ArgManager() + "-U --upgrade-strategy eager"))
        elif deploy_mode == ONLINE_DEPLOY_MODE:
            self.add_unpack_opt(OnlineInstallWhlOpt(package=package,
                                                    version=version,
                                                    no_dependent=no_dependent,
                                                    find_links=find_links,
                                                    opts=opts))
        elif deploy_mode == LOCAL_INSTALL_DEPLOY_MODE:
            self.add_pack_opt(OnlineInstallWhlOpt(package=package,
                                                  version=version,
                                                  no_dependent=no_dependent,
                                                  find_links=find_links,
                                                  opts=opts))


class _RequirementsPackage(SubModule):
    def __init__(self,
                 requirements_file_path,
                 deploy_mode=None):
        super().__init__(name=None)
        if deploy_mode is None:
            deploy_mode = DEFAULT_DEPLOY_MODE

        fs_data = ""
        # 部分情况需要序列化requirement.txt文件
        if deploy_mode != LOCAL_INSTALL_DEPLOY_MODE:
            fs = FileSerialize(requirements_file_path)
            fs_data = FLAG_FILE_SERIALIZE + fs.get_serialize_data()
        requirements_file_path = "-r " + requirements_file_path
        if deploy_mode == LOCAL_DOWNLOAD_DEPLOY_MODE:
            self.add_pack_opt(DownloadWhlOpt(opts=ArgManager() + requirements_file_path,
                                             no_dependent=False))
            self.add_unpack_opt(LocalInstallWhlOpt(package=fs_data,
                                                   no_dependent=False))
        elif deploy_mode == ONLINE_DEPLOY_MODE:
            self.add_unpack_opt(OnlineInstallWhlOpt(package=fs_data,
                                                    no_dependent=False))
        elif deploy_mode == LOCAL_INSTALL_DEPLOY_MODE:
            self.add_pack_opt(OnlineInstallWhlOpt(opts=ArgManager() + requirements_file_path,
                                                  no_dependent=False,
                                                  to_module_env_path=True))


class QPTDependencyPackage(SubModule):
    def __init__(self):
        self.level = TOP_LEVEL_REDUCE
        super().__init__(name=None)
        kernel_dependency_path = os.path.join(os.path.split(__file__)[0], "kernel_dependency.txt")
        lazy_dependency_path = os.path.join(os.path.split(__file__)[0], "qpt_lazy_dependency.txt")
        lazy_dependency_serialize = FLAG_FILE_SERIALIZE + FileSerialize(lazy_dependency_path).get_serialize_data()
        kernel = "-r " + kernel_dependency_path
        lazy = "-r " + lazy_dependency_path
        self.add_pack_opt(OnlineInstallWhlOpt(package="qpt",
                                              version=qpt_version,
                                              no_dependent=True,
                                              to_module_env_path=True))
        self.add_pack_opt(OnlineInstallWhlOpt(no_dependent=False,
                                              to_module_env_path=True,
                                              opts=ArgManager() + "-U" + kernel))
        self.add_pack_opt(DownloadWhlOpt(opts=ArgManager() + lazy,
                                         no_dependent=False))
        self.add_unpack_opt(LocalInstallWhlOpt(package=lazy_dependency_serialize,
                                               no_dependent=False))


class QPTGUIDependencyPackage(SubModule):
    def __init__(self):
        self.level = TOP_LEVEL_REDUCE
        super().__init__(name=None)
        kernel_dependency_path = os.path.join(os.path.split(__file__)[0], "kernel_dependency_GUI.txt")
        kernel = "-r " + kernel_dependency_path
        self.add_pack_opt(OnlineInstallWhlOpt(opts=ArgManager() + kernel,
                                              no_dependent=False,
                                              to_module_env_path=True))


class BatchInstallation(SubModule):
    def __init__(self):
        super().__init__()
        self.level = LOW_LEVEL
        if DEFAULT_DEPLOY_MODE == LOCAL_DOWNLOAD_DEPLOY_MODE:
            self.add_unpack_opt(BatchInstallationOpt())


class CopyWhl2PackagesOpt(SubModuleOpt):
    def __init__(self, whl_path):
        """
        适用于安装额外且单一的whl包，将whl包移动至打包后的opt/packages目录，在首次运行EXE时会自动对该包进行安装。
        :param whl_path: whl路径
        """
        super().__init__(disposable=True)
        self.whl_path = whl_path

    def act(self) -> None:
        shutil.copy(src=self.whl_path, dst=self.packages_path)


class CopyWhl2Packages(SubModule):
    def __init__(self,
                 whl_path,
                 level=GENERAL_LEVEL,
                 not_install=False,
                 opt=None):
        """
        适用于安装额外且单一的whl包，将whl包移动至打包后的opt/packages目录，在首次运行EXE时会自动对该包进行安装。
        :param whl_path: whl路径
        """
        super().__init__(name=os.path.basename(whl_path).replace(".", "")[:10], level=level)
        self.add_pack_opt(CopyWhl2PackagesOpt(whl_path))

        if not not_install:
            if opt is None:
                opt = ArgManager(["-U --force-reinstall"])
            self.add_unpack_opt(LocalInstallWhlOpt(package=whl_path, static_whl=True, opts=opt))
