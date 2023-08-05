cmake_minimum_required(VERSION 3.22)

include(${CMAKE_CURRENT_LIST_DIR}/FrameworkTargets.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/PyModelTargets.cmake)

set(CMAKE_POSITION_INDEPENDENT_CODE On)

# SystemC dependencies
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

# Find SystemC using SystemC's CMake integration
find_package(SystemCLanguage QUIET)

# Verilator is required for simulation.
find_package(verilator REQUIRED $ENV{VERILATOR_ROOT} ${VERILATOR_ROOT})

# Logging
find_package(spdlog REQUIRED)

if (SKBUILD)
  # Scikit-Build does not add your site-packages to the search path
  # automatically, so we need to add it _or_ the pybind11 specific directory
  # here.
  execute_process(
    COMMAND "${PYTHON_EXECUTABLE}" -c
            "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE _tmp_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
  list(APPEND CMAKE_PREFIX_PATH "${_tmp_dir}")
  find_package(pybind11 CONFIG REQUIRED)
else()
  if (NOT PYBIND_DIR)
    set(PYBIND_DIR "extern/pybind11")
  endif()
  add_subdirectory(${pybind11_DIR} ${CMAKE_BINARY_DIR}/pybind11)
endif()

# Abies cmake directory is one below Abies root. abies/cmake
cmake_path(GET Abies_DIR PARENT_PATH Abies_ROOT)

# Abies package structure is fixed.
set(Abies_SOURCE_DIR ${Abies_ROOT}/framework)
set(Abies_INCLUDE_DIRS ${Abies_ROOT}/include)
set(Abies_LIBRARIES Abies::PyModel Abies::Framework)
set(Abies_RTL_INCLUDE_DIRS ${Abies_ROOT}/library/rtl/include)
set(Abies_RTL_MODULE_DIRS ${Abies_ROOT}/library/rtl)

# Function to automatically configure and build abies plugins.
function(abies_add_module TARGET CPYMODULE RTL_MODULE)
    # Use pybind11 as the base module
    pybind11_add_module(${TARGET} ${CPYMODULE})

    target_include_directories(${TARGET} PRIVATE ${Abies_INCLUDE_DIRS})
    target_link_libraries(${TARGET} PRIVATE Abies::PyModel Abies::Framework)

    cmake_path(GET RTL_MODULE PARENT_PATH USER_MODULE_DIR)
    # Add the Verilated circuit to the target
    verilate(${TARGET} SYSTEMC TRACE
        SOURCES ${RTL_MODULE}
        INCLUDE_DIRS ${Abies_RTL_INCLUDE_DIRS}
        VERILATOR_ARGS -y ${Abies_RTL_MODULE_DIRS} -y ${USER_MODULE_DIR} -Wall 
        )
    # Auto-link systemc
    verilator_link_systemc(${TARGET})

    # Install targets where python needs them installed
    install(TARGETS ${TARGET} DESTINATION ${CMAKE_INSTALL_PREFIX})

endfunction()

