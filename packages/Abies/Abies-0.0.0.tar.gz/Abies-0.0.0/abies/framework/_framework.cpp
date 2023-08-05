/*
    Python bindings
*/
#include "framework.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl/filesystem.h>
#include <pybind11/numpy.h>

#include <string>

namespace py = pybind11;
using namespace abies;

PYBIND11_MODULE(_framework, m)
{
    m.doc() = "Framework Python Bindings";
    py::class_<Framework>(m, "Framework")
        .def(py::init<std::filesystem::path &>(), py::arg("log_dir") = std::filesystem::path("logs"))
        // .def("enable_tracing", &Framework::enable_tracing, py::arg("trace_dir"))
        .def("initialize", &Framework::initialize_sim, py::arg("netlist"))
        .def("run", &Framework::run, py::arg("duration") = 1)
        .def_property("log_level", &Framework::getLogLevel, &Framework::setLogLevel)
        .def_property("trace", &Framework::getTraceEnable, &Framework::setTraceEnable);
}
