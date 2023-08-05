/*
    Generated file for python bindings. Compile this function into a python extension.
*/
#include <abies/py_model.h>
#include "V{{cookiecutter.module_name}}.h"

PYBIND11_MODULE(_{{cookiecutter.module_name}}, m)
{
    // Create a pybind module using the default template.
    abies::create_pybind_module<V{{cookiecutter.module_name}}>(m);
}

// SystemC demands that this must be defined..
int sc_main(int argc, char **argv)
{
    return 0;
}