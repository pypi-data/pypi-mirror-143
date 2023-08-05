# 
# add_subdirectory(dff)
# Function to automatically configure and build abies plugins.
function(add_rtl_module TARGET CPYMODULE RTL_MODULE)
    # Use pybind11 as the base module
    pybind11_add_module(${TARGET} ${CPYMODULE})

    target_include_directories(${TARGET} PRIVATE ${Abies_INCLUDE_DIRS})
    target_link_libraries(${TARGET} PRIVATE PyModel Framework)

    cmake_path(GET CPYMODULE PARENT_PATH _CPYPARENT)
    cmake_path(GET _CPYPARENT STEM _LIBPATH)

    # Add the Verilated circuit to the target
    verilate(${TARGET} SYSTEMC TRACE
        SOURCES ${RTL_MODULE}
        INCLUDE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/rtl/include
        VERILATOR_ARGS -y ${CMAKE_CURRENT_SOURCE_DIR}/rtl -Wall 
        )
    # Auto-link systemc
    verilator_link_systemc(${TARGET})

    # Install targets where python needs them installed
    install(TARGETS ${TARGET} DESTINATION ${CMAKE_INSTALL_PREFIX}/library/${_LIBPATH})

endfunction()

add_rtl_module(_vdff vdff/_vdff.cpp rtl/dff.sv)

# add_subdirectory(vdff)
