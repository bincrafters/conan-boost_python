#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools


class BoostPythonConan(ConanFile):
    name = "boost_python"
    version = "1.67.0"
    author = "Bincrafters <bincrafters@gmail.com>"
    exports = ["LICENSE.md"]
    lib_short_names = ["python"]
    is_header_only = False

    options = {
        "shared": [True, False],
        "python_version": [
            None,
            '2.2', '2.3', '2.4', '2.5', '2.6', '2.7',
            '3.0','3.1','3.2','3.3','3.4','3.5','3.6','3.7','3.8','3.9'
            ]}
    default_options = "shared=False"

    source_only_deps = [
        "graph",
        "integer",
        "multi_index",
        "parameter",
        "property_map",
        "serialization",
        "unordered"
    ]

    requires = (
        "boost_bind/1.67.0@bincrafters/testing",
        "boost_config/1.67.0@bincrafters/testing",
        "boost_conversion/1.67.0@bincrafters/testing",
        "boost_core/1.67.0@bincrafters/testing",
        "boost_detail/1.67.0@bincrafters/testing",
        "boost_foreach/1.67.0@bincrafters/testing",
        "boost_function/1.67.0@bincrafters/testing",
        "boost_iterator/1.67.0@bincrafters/testing",
        "boost_lexical_cast/1.67.0@bincrafters/testing",
        "boost_mpl/1.67.0@bincrafters/testing",
        "boost_numeric_conversion/1.67.0@bincrafters/testing",
        "boost_package_tools/1.67.0@bincrafters/testing",
        "boost_preprocessor/1.67.0@bincrafters/testing",
        "boost_smart_ptr/1.67.0@bincrafters/testing",
        "boost_static_assert/1.67.0@bincrafters/testing",
        "boost_tuple/1.67.0@bincrafters/testing",
        "boost_type_traits/1.67.0@bincrafters/testing",
        "boost_utility/1.67.0@bincrafters/testing",
        "python_dev_config/0.3@bincrafters/stable"
    )

    def package_info_additional(self):
        if self.options.shared:
            self.cpp_info.defines.append('BOOST_PYTHON_DYNAMIC_LIB')
        else:
            self.cpp_info.defines.append('BOOST_PYTHON_STATIC_LIB')

    def package_id_additional(self):
        boost_deps_only = [dep_name for dep_name in self.info.requires.pkg_names if dep_name.startswith("boost_")]
        for dep_name in boost_deps_only:
            self.info.requires[dep_name].full_version_mode()

    def source_additional(self):
        if 'python_version' in self.options:
            if not self.options.python_version:
                self.options.python_version = self.deps_user_info['python_dev_config'].python_version
            elif self.options.python_version != self.deps_user_info['python_dev_config'].python_version:
                raise Exception("Python version does not match with configured python dev, expected %s but got %s." % (self.options.python_version, self.deps_user_info['python_dev_config'].python_version))

    # BEGIN

    url = "https://github.com/bincrafters/conan-boost_python"
    description = "Please visit http://www.boost.org/doc/libs/1_67_0"
    license = "BSL-1.0"
    short_paths = True
    generators = "boost"
    settings = "os", "arch", "compiler", "build_type"
    build_requires = "boost_generator/1.67.0@bincrafters/testing"

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
