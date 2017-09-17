#include <boost/python.hpp>

int main()
{
	boost::python::def("greet", greet);
}

