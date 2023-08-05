#pragma once

#include "framework.h"
// #include "model.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <string>

namespace abies
{
    static inline void _register_with(Framework::ModelFactory fact, Framework &f, const std::string &model_name)
    {
        f.register_model(model_name, fact);
    }

    template <class BaseModel>
    class TraceWrap : public BaseModel
    {
    public:
        using BaseModel::BaseModel;

        void trace(sc_trace_file *tfp) const
        {
            sc_trace(tfp, BaseModel::clk, std::string(BaseModel::name()) + ".clk");
            sc_trace(tfp, BaseModel::rst, std::string(BaseModel::name()) + ".rst");
            sc_trace(tfp, BaseModel::ce, std::string(BaseModel::name()) + ".ce");
            sc_trace(tfp, BaseModel::d, std::string(BaseModel::name()) + ".d");
            sc_trace(tfp, BaseModel::q, std::string(BaseModel::name()) + ".q");
        }
    };

    template <typename ModelType>
    Framework::ModelPtr default_model_factory(const char *model_name)
    {
        return std::make_shared<ModelType>(model_name);
    }

    template <typename ModelType>
    void create_pybind_module(pybind11::module &m, Framework::ModelFactory fact)
    {
        m.doc() = "Python Bindings";

        std::function<void(Framework &, const std::string &)> reg_func = std::bind(&_register_with, fact, std::placeholders::_1, std::placeholders::_2);
        m.def("register_with", reg_func,
              pybind11::arg("framework"), pybind11::arg("name"));

        // Use the base model class for the framework version.
        m.def("framework_version", Framework::version);
    }

    template <typename M>
    void create_pybind_module(pybind11::module &m)
    {
        create_pybind_module<TraceWrap<M>>(m, default_model_factory<TraceWrap<M>>);
    }
}