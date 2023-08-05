#include "py_model.h"
#include "Vdff.h"

PYBIND11_MODULE(_vdff, m)
{
    // Create a pybind module using the default template.
    abies::create_pybind_module<Vdff>(m);
}
