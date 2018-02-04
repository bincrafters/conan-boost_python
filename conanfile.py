#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
from io import StringIO
import os


class BoostPythonConan(ConanFile):
    name = "boost_python"
    version = "1.65.1"
    url = "https://github.com/bincrafters/conan-boost_python"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md"]
    lib_short_names = ["python"]
    is_header_only = False
    
    options = {"shared": [True, False], "python": "ANY"}
    default_options = "shared=False", "python=python"

    source_only_deps = ["graph", "multi_index", "parameter", 
    "property_map", "serialization", "unordered"]
    
    requires = (
        "boost_package_tools/1.65.1@bincrafters/testing",
        "boost_bind/1.65.1@bincrafters/testing",
        "boost_config/1.65.1@bincrafters/testing",
        "boost_conversion/1.65.1@bincrafters/testing",
        "boost_core/1.65.1@bincrafters/testing",
        "boost_detail/1.65.1@bincrafters/testing",
        "boost_foreach/1.65.1@bincrafters/testing",
        "boost_function/1.65.1@bincrafters/testing",
        "boost_iterator/1.65.1@bincrafters/testing",
        "boost_lexical_cast/1.65.1@bincrafters/testing",
        "boost_mpl/1.65.1@bincrafters/testing",
        "boost_numeric_conversion/1.65.1@bincrafters/testing",
        "boost_preprocessor/1.65.1@bincrafters/testing",
        "boost_smart_ptr/1.65.1@bincrafters/testing",
        "boost_static_assert/1.65.1@bincrafters/testing",
        "boost_tuple/1.65.1@bincrafters/testing",
        "boost_type_traits/1.65.1@bincrafters/testing",
        "boost_utility/1.65.1@bincrafters/testing"
    )

    def package_info_additional(self):
        self.cpp_info.includedirs.append(self.python_include)
        self.cpp_info.libdirs.append(os.path.dirname(self.python_lib))
        self.cpp_info.libs.append(os.path.basename(self.python_lib))
            
    def package_id_additional(self):
        self.info.options.python = "python-" + self.python_version

        boost_deps_only = [dep_name for dep_name in self.info.requires.pkg_names if dep_name.startswith("boost_")]
        for dep_name in boost_deps_only:
            self.info.requires[dep_name].full_version_mode()

    def _is_amd64_to_i386(self):
        return self.settings.arch == "x86" and tools.detected_architecture() == "x86_64"

    def system_requirements(self):
        if self.settings.os == "Linux":
            arch = ":i386" if self._is_amd64_to_i386() else ""
            package_tool = tools.SystemPackageTool()
            package_tool.install("python-dev%s" % arch)
    
    @property
    def python_exec(self):
        try:
            pyexec = str(self.options.python)
            output = StringIO()
            self.run('{0} -c "import sys; print(sys.executable)"'.format(pyexec), output=output)
            return output.getvalue().strip().replace("\\", "/")
        except:
            return ""

    @property
    def python_include(self):
        pyinclude = self.get_python_path("include")
        if not os.path.exists(os.path.join(pyinclude, 'pyconfig.h')):
            return ""
        else:
            return pyinclude.replace('\\', '/')

    @property
    def python_version(self):
        cmd = "from sys import *; print('%d.%d' % (version_info[0],version_info[1]))"
        return self.run_python_command(cmd)

    @property
    def python_version_nodot(self):
        cmd = "from sys import *; print('%d%d' % (version_info[0],version_info[1]))"
        return self.run_python_command(cmd)

    @property
    def python_lib(self):
        py_stdlib = self.get_python_path("stdlib").replace('\\', '/')
        if self.settings.os == "Windows":
            py_stdlib = os.path.join(os.path.dirname(py_stdlib), "libs", "python"+self.python_version_nodot+".lib")
        return py_stdlib

    def get_python_path(self, dir_name):
        cmd = "import sysconfig; print(sysconfig.get_path('{0}'))".format(dir_name)
        return self.run_python_command(cmd)

    def run_python_command(self, cmd):
        pyexec = self.python_exec
        if pyexec:
            output = StringIO()
            self.run('{0} -c "{1}"'.format(pyexec, cmd), output=output)
            return output.getvalue().strip()
        else:
            return ""

    # BEGIN

    description = "Please visit http://www.boost.org/doc/libs/1_65_1"
    license = "BSL-1.0"
    short_paths = True
    generators = "boost"
    settings = "os", "arch", "compiler", "build_type"
    build_requires = "boost_generator/1.65.1@bincrafters/testing"

    def package_id(self):
        getattr(self, "package_id_additional", lambda:None)()

    def source(self):
        with tools.pythonpath(self):
            import boost_package_tools  # pylint: disable=F0401
            boost_package_tools.source(self)
        getattr(self, "source_additional", lambda:None)()

    def build(self):
        with tools.pythonpath(self):
            import boost_package_tools  # pylint: disable=F0401
            boost_package_tools.build(self)
        getattr(self, "build_additional", lambda:None)()

    def package(self):
        with tools.pythonpath(self):
            import boost_package_tools  # pylint: disable=F0401
            boost_package_tools.package(self)
        getattr(self, "package_additional", lambda:None)()

    def package_info(self):
        with tools.pythonpath(self):
            import boost_package_tools  # pylint: disable=F0401
            boost_package_tools.package_info(self)
        getattr(self, "package_info_additional", lambda:None)()



    # END
