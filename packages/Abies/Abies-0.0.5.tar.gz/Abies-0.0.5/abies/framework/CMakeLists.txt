# Simulation Framework library. This will load plugins and run simulations.
add_library(Framework src/framework.cpp)

target_link_libraries(Framework PUBLIC spdlog::spdlog SystemC::systemc)

target_include_directories(Framework PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/abies>
)

install(TARGETS Framework
        EXPORT FrameworkTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(FILES include/framework.h DESTINATION include/abies)

# Install cmake targets. This lets you easily link to this library.
install(EXPORT FrameworkTargets
        FILE FrameworkTargets.cmake
        NAMESPACE Abies::
        DESTINATION cmake # Install under abies/cmake
)

# PyModel plugin base class.
add_library(PyModel INTERFACE)

target_link_libraries(PyModel INTERFACE pybind11::module Framework)

target_include_directories(PyModel INTERFACE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/abies>
)

install(TARGETS PyModel
        EXPORT PyModelTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(FILES include/py_model.h DESTINATION include/abies)

install(EXPORT PyModelTargets
        FILE PyModelTargets.cmake
        NAMESPACE Abies::
        DESTINATION cmake # Using CMAKE_INSTALL_PREFIX makes things install weird.
)

# Python bindings
pybind11_add_module(_framework src/_framework.cpp)

target_link_libraries(_framework PUBLIC SystemC::systemc Framework PyModel)

install(TARGETS _framework DESTINATION framework)
