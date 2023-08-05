# Function to configure and build abies library modules.
# Arg1: library name, typically with an _ prefix.
# Arg2: pybind11 C++ file. typically with an _
# Arg3: rtl file containing top module to be built into a plugin model.
function(add_rtl_module RTL_MODULE)
    
    cmake_path(GET RTL_MODULE STEM RTL_STEM)
    set(TARGET _${RTL_STEM})
    set(CPYMODULE src/${TARGET}.cpp)

    # Use pybind11 as the base module
    pybind11_add_module(${TARGET} ${CPYMODULE})

    target_include_directories(${TARGET} PRIVATE ${Abies_INCLUDE_DIRS})
    target_link_libraries(${TARGET} PRIVATE PyModel Framework)

    # Add the Verilated circuit to the target
    verilate(${TARGET} SYSTEMC TRACE
        SOURCES ${RTL_MODULE}
        INCLUDE_DIRS rtl/include
        VERILATOR_ARGS -y rtl -Wall 
        )
    # Link systemc
    verilator_link_systemc(${TARGET})

    # Install targets where python needs them installed
    install(TARGETS ${TARGET} DESTINATION library/${RTL_STEM})

endfunction()

add_rtl_module(rtl/dff.sv)

# add_subdirectory(vdff)
