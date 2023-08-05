#include "framework.h"
#include "spdlog/sinks/basic_file_sink.h"

static abies::Framework *sim_framework = nullptr;
static int sim_duration = 0;

namespace abies
{
    Framework::Framework(std::filesystem::path &log_dir)
    {
        auto logfile = log_dir / "framework.log";
        logger = spdlog::get("framework");
        if (!logger)
        {
            logger = spdlog::basic_logger_mt("framework", logfile);
        }

        auto tracefile = log_dir / "framework";

        // Disable info messages about timescale..
        sc_report_handler::set_actions(SC_INFO, SC_DO_NOTHING);
        tfp = sc_create_vcd_trace_file(tracefile.c_str());
        // tfp->set_time_unit(1.0, SC_NS);
    }

    Framework::~Framework()
    {
        sc_close_vcd_trace_file(tfp);
    }

    void Framework::register_model(const std::string &model_name, ModelFactory &fact)
    {
        SPDLOG_LOGGER_DEBUG(logger, "Framework register_model");
        all_models[model_name] = fact;
    }

    Framework::ModelPtr Framework::get_model(const std::string &model_name, const std::string &instance_name)
    {
        SPDLOG_LOGGER_DEBUG(logger, "Framework get_model");
        auto model = all_models[model_name](instance_name.c_str());

        return model;
    }

    void Framework::initialize_sim(std::vector<std::tuple<std::string, std::string>> netlist)
    {
        SPDLOG_LOGGER_DEBUG(logger, "Framework initialize_sim");
        for (auto node : netlist)
        {
            auto model = get_model(std::get<0>(node), std::get<1>(node));
            all_instances.push_back(model);
        }
    }

    void Framework::run(int duration)
    {
        SPDLOG_LOGGER_DEBUG(logger, "Run");

        for (auto i : all_instances)
        {
            SPDLOG_LOGGER_DEBUG(logger, "instance: {}", std::string(i->name()));
        }

        // Assign the static simulation to this instance.
        // This seems naughty but idk how to do this with systemc.
        sim_duration = duration;
        sim_framework = this;
        sc_elab_and_sim(0, 0);
    }

    // Python properties
    void Framework::setLogLevel(const std::string &log_level)
    {
        logger->set_level(spdlog::level::from_str(log_level));
    }

    std::string Framework::getLogLevel(void)
    {
        return spdlog::level::to_short_c_str(logger->level());
    }

    void Framework::setTraceEnable(const bool enable)
    {
        trace_enable = enable;
    }

    bool Framework::getTraceEnable(void)
    {
        return trace_enable;
    }
} // namespace abies

int sc_main(int argc, char **argv)
{
    static int called_n_times = 1;

    // initialize clock
    sc_clock clk("clk", 10, SC_NS, 0.5, 0.0, SC_NS, true);
    sc_signal<bool> rst;
    sc_signal<bool> ce;

    std::vector<sc_signal<uint32_t>> all_signals(sim_framework->all_instances.size() + 1);

    int bus_id = 0;

    for (auto i : sim_framework->all_instances)
    {
        // Attach signals.
        (*i)(clk, rst, ce, all_signals[bus_id], all_signals[bus_id + 1]);

        // Trace signals
        if (sim_framework->getTraceEnable())
        {
            i->trace(sim_framework->tfp);
        }
        bus_id++;
    }

    all_signals[0] = 42;
    rst = 1;
    ce = 1;
    sc_start(100, SC_NS);

    rst = 0;

    sc_start(sim_duration, SC_NS);

    return 0;
}
