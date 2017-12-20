from conans import ConanFile
from io import StringIO


class BoostPythonConan(ConanFile):
    name = "Boost.Python"
    version = "1.65.1"

    options = {"shared": [True, False], "python": "ANY"}
    default_options = "shared=False", "python=python"

    source_only_deps = ["graph", "multi_index", "parameter", "property_map", "serialization", "unordered"]
    requires = \
        "Boost.Bind/1.65.1@bincrafters/testing", \
        "Boost.Config/1.65.1@bincrafters/testing", \
        "Boost.Conversion/1.65.1@bincrafters/testing", \
        "Boost.Core/1.65.1@bincrafters/testing", \
        "Boost.Detail/1.65.1@bincrafters/testing", \
        "Boost.Foreach/1.65.1@bincrafters/testing", \
        "Boost.Function/1.65.1@bincrafters/testing", \
        "Boost.Iterator/1.65.1@bincrafters/testing", \
        "Boost.Lexical_Cast/1.65.1@bincrafters/testing", \
        "Boost.Mpl/1.65.1@bincrafters/testing", \
        "Boost.Numeric_Conversion/1.65.1@bincrafters/testing", \
        "Boost.Preprocessor/1.65.1@bincrafters/testing", \
        "Boost.Smart_Ptr/1.65.1@bincrafters/testing", \
        "Boost.Static_Assert/1.65.1@bincrafters/testing", \
        "Boost.Tuple/1.65.1@bincrafters/testing", \
        "Boost.Type_Traits/1.65.1@bincrafters/testing", \
        "Boost.Utility/1.65.1@bincrafters/testing"

    lib_short_names = ["python"]
    is_header_only = False

    def package_info_after(self):
        import os.path
        self.cpp_info.includedirs.append(self.python_include)
        self.cpp_info.libdirs.append(os.path.dirname(self.python_lib))
        self.cpp_info.libs.append(os.path.basename(self.python_lib))

    def package_id_after(self):
        self.info.options.python = "python-" + self.python_version

    def _is_amd64_to_i386(self):
        from conans import tools
        return self.settings.arch == "x86" and tools.detected_architecture() == "x86_64"

    def system_requirements(self):
        if self.settings.os == "Linux":
            arch = ":i386" if self._is_amd64_to_i386() else ""
            from conans import tools
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
        import os.path
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

    url = "https://github.com/bincrafters/conan-boost-python"
    description = "Please visit http://www.boost.org/doc/libs/1_65_1"
    license = "www.boost.org/users/license.html"
    build_requires = "Boost.Generator/1.65.1@bincrafters/testing"
    short_paths = True
    generators = "boost"
    settings = "os", "arch", "compiler", "build_type"
    exports = "boostgenerator.py"

    def package_id(self):
        getattr(self, "package_id_after", lambda:None)()
    def source(self):
        self.call_patch("source")
    def build(self):
        self.call_patch("build")
    def package(self):
        self.call_patch("package")
    def package_info(self):
        self.call_patch("package_info")
    def call_patch(self, method, *args):
        if not hasattr(self, '__boost_conan_file__'):
            try:
                from conans import tools
                with tools.pythonpath(self):
                    import boostgenerator  # pylint: disable=F0401
                    boostgenerator.BoostConanFile(self)
            except Exception as e:
                self.output.error("Failed to import boostgenerator for: "+str(self)+" @ "+method.upper())
                raise e
        return getattr(self, method, lambda:None)(*args)
    @property
    def env(self):
        import os.path
        result = super(self.__class__, self).env
        result['PYTHONPATH'] = [os.path.dirname(__file__)] + result.get('PYTHONPATH',[])
        return result
    @property
    def build_policy_missing(self):
        return (getattr(self, 'is_in_cycle_group', False) and not getattr(self, 'is_header_only', True)) or super(self.__class__, self).build_policy_missing

    # END
