cmake_minimum_required(VERSION 3.22)
project({{cookiecutter.module_name}})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(Python 3.10 COMPONENTS Interpreter Development)

# Find Abies from python if Abies_ROOT is not given.
if (NOT Abies_ROOT)
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -c
            "import abies; print(abies.get_cmake_dir())"
    OUTPUT_VARIABLE _abies_cmake_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
    message(${_abies_cmake_dir})
  list(APPEND CMAKE_PREFIX_PATH ${_abies_cmake_dir})
else()
  # Root of source repository was supplied to CMake.
  list(APPEND CMAKE_PREFIX_PATH ${Abies_ROOT}/abies/cmake)
endif()

# Abies CMake package contains cmake functions to create libraries.
find_package(Abies REQUIRED)

# Verilates the model, then creates the pybind module. Installs everything. Easy.
abies_add_module(
  _{{cookiecutter.module_name}} # Module library.
  {{cookiecutter.module_name}}/_{{cookiecutter.module_name}}.cpp # Pybind11 C++ file.
  {{cookiecutter.module_name}}/rtl/{{cookiecutter.module_name}}.sv # RTL file containing top design.
)
