cmake_minimum_required(VERSION 3.22)

include(${CMAKE_CURRENT_LIST_DIR}/FrameworkTargets.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/PyModelTargets.cmake)

# SystemC dependencies
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

# Find SystemC using SystemC's CMake integration
find_package(SystemCLanguage REQUIRED QUIET)

# Verilator is required for simulation.
find_package(verilator REQUIRED $ENV{VERILATOR_ROOT} ${VERILATOR_ROOT})

# Logging
find_package(spdlog REQUIRED)

if (SKBUILD)
  # Locate pybind11 cmake directory.
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -c
            "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE _pybind11_cmake_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
  list(APPEND CMAKE_PREFIX_PATH "${_pybind11_cmake_dir}")
  find_package(pybind11 CONFIG REQUIRED)
else()
  if (NOT PYBIND_DIR)
    # Default location if using git submodules.
    set(PYBIND_DIR "extern/pybind11")
  endif()
  add_subdirectory(${pybind11_DIR} ${CMAKE_BINARY_DIR}/pybind11)
endif()

# Abies cmake directory is one below Abies root. abies/cmake
cmake_path(GET Abies_DIR PARENT_PATH Abies_ROOT)

# Abies package structure is fixed.
set(Abies_SOURCE_DIR ${Abies_ROOT}/framework/src)
set(Abies_INCLUDE_DIRS ${Abies_ROOT}/include)
set(Abies_LIBRARIES Abies::PyModel Abies::Framework)
set(Abies_RTL_INCLUDE_DIRS ${Abies_ROOT}/library/rtl/include)
set(Abies_RTL_MODULE_DIRS ${Abies_ROOT}/library/rtl)

# Function to automatically configure and build abies plugins.
function(abies_add_module RTL_MODULE)
    
    cmake_path(GET RTL_MODULE STEM LAST_ONLY RTL_STEM)
    set(TARGET _${RTL_STEM})
    set(CPYMODULE ${RTL_STEM}/src/${TARGET}.cpp)

    # Use pybind11 as the base module
    pybind11_add_module(${TARGET} ${CPYMODULE})

    target_include_directories(${TARGET} PRIVATE ${Abies_INCLUDE_DIRS})
    target_link_libraries(${TARGET} PRIVATE Abies::PyModel Abies::Framework)

    # Assume all user modules are in the same directory.
    cmake_path(GET RTL_MODULE PARENT_PATH USER_MODULE_DIR)

    # Add the Verilated circuit to the target
    verilate(${TARGET} SYSTEMC TRACE
        SOURCES ${RTL_MODULE}
        INCLUDE_DIRS ${Abies_RTL_INCLUDE_DIRS} ${USER_MODULE_DIR}
        VERILATOR_ARGS -y ${Abies_RTL_MODULE_DIRS} -Wall 
        )
    # link systemc
    verilator_link_systemc(${TARGET})

    # Install targets where python needs them installed
    install(TARGETS ${TARGET} DESTINATION ${TARGET})

endfunction()

