#pragma once

#include <systemc.h>
#include <spdlog/spdlog.h>

#include <vector>
#include <functional>
#include <map>
#include <tuple>
#include <filesystem>

namespace abies
{
    class Framework
    {
        static const int _version = 0;

    public:
        static int version(void)
        {
            return _version;
        }

        Framework(std::filesystem::path &log_dir);
        ~Framework();

        typedef std::shared_ptr<sc_core::sc_module> ModelPtr;
        // using ModelPtr = std::shared_ptr<Model>;
        // Arguments: Model Name
        typedef std::function<ModelPtr(const char *)> ModelFactory;

        // Add a model factory to the registry.
        void register_model(const std::string &model_name, ModelFactory &fact);

        // Get an instance of a model.
        ModelPtr get_model(const std::string &model_name, const std::string &instance_name);

        // Construct simulation from a netlist.
        void initialize_sim(std::vector<std::tuple<std::string, std::string>> netlist);

        // Run the simulation for a specified time.
        void run(int duration = 1);

        // Properties in Python.
        void setLogLevel(const std::string &log_level);
        std::string getLogLevel(void);
        void setTraceEnable(const bool enable);
        bool getTraceEnable(void);

    public:
        std::map<const std::string, ModelFactory> all_models;
        std::vector<ModelPtr> all_instances;

        sc_trace_file *tfp;

    private:
        std::shared_ptr<spdlog::logger> logger;

        bool trace_enable = false;
    };

}
