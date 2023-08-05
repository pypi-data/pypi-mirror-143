/*
    Generated file for python bindings. Compile this function into a python extension.
*/
#include "framework.h"
#include "py_model.h"
#include "dff.h"

using namespace abies;

PYBIND11_MODULE(_dff, m)
{
    // Create an instance of the class, so pybind11 has information about it.
    // auto _frameworkInst = pybind11::class_<abies::Framework>(m, "Framework");

    // Create a pybind module using the default template.
    create_pybind_module<dff>(m, default_model_factory<dff>);
}
