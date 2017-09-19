from conans import ConanFile, tools, os

class BoostPythonConan(ConanFile):
    name = "Boost.Python"
    version = "1.65.1"
    generators = "boost" 
    settings = "os", "arch", "compiler", "build_type"
    short_paths = True
    url = "https://github.com/bincrafters/conan-boost-python"
    description = "Please visit http://www.boost.org/doc/libs/1_65_1/libs/libraries.htm"
    license = "www.boost.org/users/license.html"
    lib_short_names = ["python"]
    options = {"shared": [True, False], "python": "ANY"}
    default_options = "shared=False", "python=python"
    source_only_deps = ["graph", "multi_index", "parameter","property_map",
        "serialization", "unordered"]
    build_requires = "Boost.Generator/1.65.1@bincrafters/stable" 
    requires =  "Boost.Bind/1.65.1@bincrafters/stable", \
                      "Boost.Config/1.65.1@bincrafters/stable", \
                      "Boost.Conversion/1.65.1@bincrafters/stable", \
                      "Boost.Core/1.65.1@bincrafters/stable", \
                      "Boost.Detail/1.65.1@bincrafters/stable", \
                      "Boost.Foreach/1.65.1@bincrafters/stable", \
                      "Boost.Function/1.65.1@bincrafters/stable", \
                      "Boost.Iterator/1.65.1@bincrafters/stable", \
                      "Boost.Lexical_Cast/1.65.1@bincrafters/stable", \
                      "Boost.Mpl/1.65.1@bincrafters/stable", \
                      "Boost.Numeric_Conversion/1.65.1@bincrafters/stable", \
                      "Boost.Preprocessor/1.65.1@bincrafters/stable", \
                      "Boost.Smart_Ptr/1.65.1@bincrafters/stable", \
                      "Boost.Static_Assert/1.65.1@bincrafters/stable", \
                      "Boost.Tuple/1.65.1@bincrafters/stable", \
                      "Boost.Type_Traits/1.65.1@bincrafters/stable", \
                      "Boost.Utility/1.65.1@bincrafters/stable"

                      #bind3 config0 conversion5 core2 detail5 foreach8 function5 iterator5 lexical_cast8 mpl5 numeric~conversion6 preprocessor0 smart_ptr4 static_assert1 tuple4 type_traits3 utility5

    def source(self):
        boostorg_github = "https://github.com/boostorg"
        archive_name = "boost-" + self.version
        for lib_short_name in self.lib_short_names+self.source_only_deps:
            tools.get("{0}/{1}/archive/{2}.tar.gz"
                .format(boostorg_github, lib_short_name, archive_name))
            os.rename(lib_short_name + "-" + archive_name, lib_short_name)

    def build(self):
        self.run(self.deps_user_info['Boost.Generator'].b2_command
            + ' ' + ' '.join('include=' + dep + '/include' for dep in self.source_only_deps))

    def package(self):
        self.copy(pattern="*", dst="lib", src="stage/lib")
        for lib_short_name in self.lib_short_names:
            include_dir = os.path.join(lib_short_name, "include")
            self.copy(pattern="*", dst="include", src=include_dir)

    def package_info(self):
        self.user_info.lib_short_names = ",".join(self.lib_short_names)
        self.cpp_info.libs = self.collect_libs()
        self.cpp_info.defines.append("BOOST_ALL_NO_LIB=1")

    def package_id(self):
        class get_pyver():
            def __init__(self):
                self.value = ""
            def write(self,m):
                self.value = self.value+m.strip()
        pyver = get_pyver()
        self.run(
            '''{0} -c "from sys import *; print('%d.%d' % (version_info[0],version_info[1]))"'''.format(self.info.options.python),
            output=pyver)
        self.info.options.python = "python-"+pyver.value
