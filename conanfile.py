#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import python_requires


base = python_requires("boost_base/2.0.0@bincrafters/testing")


class BoostPythonConan(base.BoostBaseConan):
    name = "boost_python"
    version = "1.70.0"
    options = {
        "python_version": [
            None, '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '3.0', '3.1',
            '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9']
    }

    def requirements(self):
        super(BoostPythonConan, self).requirements()
        self.requires("python_dev_config/0.6@bincrafters/stable")

    def config_options(self):
        super(BoostPythonConan, self).config_options()
        if 'python_version' in self.options:
            if self.options.python_version and self.options.python_version != self.deps_user_info['python_dev_config'].python_version:
                raise Exception(
                    "Python version does not match with configured python dev, expected %s but got %s." % (
                        self.options.python_version, self.deps_user_info['python_dev_config'].python_version))

    def package_info(self):
        super(BoostPythonConan, self).package_info()
        if self.options.shared:
            self.cpp_info.defines.append('BOOST_PYTHON_DYNAMIC_LIB')
            self.cpp_info.defines.append('BOOST_NUMPY_DYNAMIC_LIB')
        else:
            self.cpp_info.defines.append('BOOST_PYTHON_STATIC_LIB')
            self.cpp_info.defines.append('BOOST_NUMPY_STATIC_LIB')

    def package_id(self):
        super(BoostPythonConan, self).package_id()
        self.info.options.python_version \
            = "python-" + str(self.options.python_version)
