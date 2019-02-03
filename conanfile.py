#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import python_requires


base = python_requires("boost_base/1.69.0@bincrafters/stable")

class BoostPythonConan(base.BoostBaseConan):
    name = "boost_python"
    version = "1.69.0"
    url = "https://github.com/bincrafters/conan-boost_python"
    lib_short_names = ["python"]
    options = {
        "python_version": [None, '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '3.0', '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9'],
        "shared": [True, False]
    }
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
    b2_requires = [
        "boost_bind",
        "boost_config",
        "boost_conversion",
        "boost_core",
        "boost_detail",
        "boost_foreach",
        "boost_function",
        "boost_iterator",
        "boost_lexical_cast",
        "boost_mpl",
        "boost_numeric_conversion",
        "boost_preprocessor",
        "boost_smart_ptr",
        "boost_static_assert",
        "boost_tuple",
        "boost_type_traits",
        "boost_utility"
    ]

    def requirements_additional(self):
        self.requires("python_dev_config/0.5@bincrafters/stable")

    def config_options_additional(self):
        if 'python_version' in self.options:
            if self.options.python_version and self.options.python_version != self.deps_user_info['python_dev_config'].python_version:
                raise Exception("Python version does not match with configured python dev, expected %s but got %s." % (self.options.python_version, self.deps_user_info['python_dev_config'].python_version))

    def package_info_additional(self):
        if self.options.shared:
            self.cpp_info.defines.append('BOOST_PYTHON_DYNAMIC_LIB')
        else:
            self.cpp_info.defines.append('BOOST_PYTHON_STATIC_LIB')

    def package_id_additional(self):
        self.info.options.python_version = "python-" + str(self.options.python_version)
