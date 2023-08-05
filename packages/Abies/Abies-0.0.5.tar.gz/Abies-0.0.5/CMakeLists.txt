cmake_minimum_required(VERSION 3.22)
project(Abies)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_POSITION_INDEPENDENT_CODE On)

# Find python
find_package(Python 3.10 REQUIRED COMPONENTS Interpreter Development)

# SystemC dependencies
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

# Find verilator
find_package(verilator REQUIRED $ENV{VERILATOR_ROOT} ${VERILATOR_ROOT})

# Find SystemC using SystemC's CMake integration
find_package(SystemCLanguage REQUIRED QUIET)

# Logging
find_package(spdlog REQUIRED)

if(SKBUILD)
  # Scikit-Build does not add your site-packages to the search path
  # automatically, so we need to add it _or_ the pybind11 specific directory
  # here.
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -c
            "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE _tmp_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
  list(APPEND CMAKE_PREFIX_PATH "${_tmp_dir}")
  find_package(pybind11 CONFIG REQUIRED)
else()
  # Use a git submodule
  add_subdirectory(extern/pybind11)
endif()

# Add the main Abies package.
add_subdirectory(abies)
