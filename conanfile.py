#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
from io import StringIO
import os


class BoostPythonConan(ConanFile):
    name = "boost_python"
    version = "1.66.0"
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
        "boost_package_tools/1.66.0@bincrafters/stable",
        "boost_bind/1.66.0@bincrafters/stable",
        "boost_config/1.66.0@bincrafters/stable",
        "boost_conversion/1.66.0@bincrafters/stable",
        "boost_core/1.66.0@bincrafters/stable",
        "boost_detail/1.66.0@bincrafters/stable",
        "boost_foreach/1.66.0@bincrafters/stable",
        "boost_function/1.66.0@bincrafters/stable",
        "boost_iterator/1.66.0@bincrafters/stable",
        "boost_lexical_cast/1.66.0@bincrafters/stable",
        "boost_mpl/1.66.0@bincrafters/stable",
        "boost_numeric_conversion/1.66.0@bincrafters/stable",
        "boost_preprocessor/1.66.0@bincrafters/stable",
        "boost_smart_ptr/1.66.0@bincrafters/stable",
        "boost_static_assert/1.66.0@bincrafters/stable",
        "boost_tuple/1.66.0@bincrafters/stable",
        "boost_type_traits/1.66.0@bincrafters/stable",
        "boost_utility/1.66.0@bincrafters/stable"
    )

    def package_info_additional(self):
        self.cpp_info.includedirs.append(self.python_include)
        self.cpp_info.libdirs.append(os.path.dirname(self.python_lib))
        self.cpp_info.libs.append(os.path.basename(self.python_lib))

    def package_id_additional(self):
        self.info.options.python = "python-" + self.python_version

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
    def python_lib(self):
        return self.get_python_path("stdlib").replace('\\', '/')

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

    description = "Please visit http://www.boost.org/doc/libs/1_66_0"
    license = "BSL-1.0"
    short_paths = True
    generators = "boost"
    settings = "os", "arch", "compiler", "build_type"
    build_requires = "boost_generator/1.66.0@bincrafters/stable"

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
