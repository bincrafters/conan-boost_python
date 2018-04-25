project(test_package CXX)
cmake_minimum_required(VERSION 3.1.2)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(MPI)

file(GLOB SOURCE_FILES *.cpp)

add_executable(${CMAKE_PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${CMAKE_PROJECT_NAME} 
  CONAN_PKG::boost_bind
  CONAN_PKG::boost_config
  CONAN_PKG::boost_conversion
  CONAN_PKG::boost_core
  CONAN_PKG::boost_detail
  CONAN_PKG::boost_foreach
  CONAN_PKG::boost_function
  CONAN_PKG::boost_iterator
  CONAN_PKG::boost_lexical_cast
  CONAN_PKG::boost_mpl
  CONAN_PKG::boost_numeric_conversion
  CONAN_PKG::boost_preprocessor
  CONAN_PKG::boost_python
  CONAN_PKG::boost_smart_ptr
  CONAN_PKG::boost_static_assert
  CONAN_PKG::boost_tuple
  CONAN_PKG::boost_type_traits
  CONAN_PKG::boost_utility)
set_property(TARGET ${CMAKE_PROJECT_NAME} PROPERTY CXX_STANDARD 11)

if(MPI_CXX_FOUND)
  target_link_libraries(${CMAKE_PROJECT_NAME} CONAN_PKG::openmpi)
endif(MPI_CXX_FOUND)
