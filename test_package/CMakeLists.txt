project(test_package CXX)
cmake_minimum_required(VERSION 3.1.2)


set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(Python3 COMPONENTS Interpreter Development Compiler)
find_package(MPI)

file(GLOB SOURCE_FILES *.cpp)

add_executable(${CMAKE_PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${CMAKE_PROJECT_NAME}
  CONAN_PKG::boost_python)
set_property(TARGET ${CMAKE_PROJECT_NAME} PROPERTY CXX_STANDARD 11)

if(MPI_CXX_FOUND)
  target_link_libraries(${CMAKE_PROJECT_NAME} CONAN_PKG::openmpi)
endif(MPI_CXX_FOUND)
