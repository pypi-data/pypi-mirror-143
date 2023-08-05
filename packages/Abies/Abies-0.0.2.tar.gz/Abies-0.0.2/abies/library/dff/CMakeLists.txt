
pybind11_add_module(_dff ${CMAKE_CURRENT_LIST_DIR}/_dff.cpp)
target_link_libraries(_dff PRIVATE framework)
install(TARGETS _dff DESTINATION ${CMAKE_INSTALL_PREFIX}/library/dff)
