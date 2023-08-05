# Simulation Framework library. This will load plugins and run simulations.
add_library(Framework framework.cpp)
target_link_libraries(Framework PUBLIC spdlog::spdlog SystemC::systemc)
target_include_directories(Framework PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
  $<INSTALL_INTERFACE:include>
)

# Is all this necessary cmake?
install(TARGETS Framework
        EXPORT FrameworkTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
# Install public headers
install(FILES framework.h DESTINATION include/abies)
# Install cmake targets. This lets you easily link to this library.
install(EXPORT FrameworkTargets
        FILE FrameworkTargets.cmake
        NAMESPACE Abies::
        DESTINATION cmake
)

# PyModel plugin base class.
add_library(PyModel INTERFACE)
target_link_libraries(PyModel INTERFACE pybind11::module Framework)
target_include_directories(PyModel INTERFACE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
  $<INSTALL_INTERFACE:include>
)
install(TARGETS PyModel
        EXPORT PyModelTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
install(FILES py_model.h DESTINATION include/abies)

install(EXPORT PyModelTargets
        FILE PyModelTargets.cmake
        NAMESPACE Abies::
        DESTINATION cmake
)

# Python bindings
pybind11_add_module(_framework _framework.cpp)
target_link_libraries(_framework PUBLIC SystemC::systemc Framework PyModel)
message("Framework Install Prefix: ${CMAKE_INSTALL_PREFIX}")
install(TARGETS _framework DESTINATION framework)
