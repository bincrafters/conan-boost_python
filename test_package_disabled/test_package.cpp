#include <boost/python.hpp>
#include <cstdio>

namespace python = boost::python;

extern "C" void greet()
{
	std::puts("Greet.");
}

BOOST_PYTHON_MODULE(embedded_hello)
{
	python::def("greet",greet);
}

int main()
{
	Py_Initialize();
	if (PyImport_AppendInittab("embedded_hello", initembedded_hello) == -1)
		throw std::runtime_error("Failed");
	python::object main = python::import("__main__");
	python::object global(main.attr("__dict__"));
	python::object result = python::exec(
		"from embedded_hello import *        \n"
		"greet()\n",
		global, global);
}
