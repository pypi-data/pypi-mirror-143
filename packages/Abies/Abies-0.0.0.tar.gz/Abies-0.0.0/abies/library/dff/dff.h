#pragma once

#include "framework.h"

#include <systemc.h>
#include <iostream>
#include <spdlog/spdlog.h>

// namespace abies
// {
SC_MODULE(dff)
{
public:
    sc_in_clk clk;
    sc_in<bool> rst;
    sc_in<bool> ce;
    sc_in<uint32_t> d;
    sc_out<uint32_t> q;
    // sc_port<abies::AxisSlave> audio_in;
    // sc_port<abies::AxisMaster> audio_out;

    void handle()
    {
        wait();
        while (true)
        {
            if (rst)
            {
            }
            else if (ce)
            {
                // uint32_t rdat;
                // audio_in->read(&rdat);
                q = d;
                // SPDLOG_LOGGER_TRACE(logger, "d: {}, q: {}", d, q);
                // std::cout << "Rdat: " << rdat << std::endl;
                // audio_out->write(&rdat);
            }
            wait();
        }
    }

    SC_CTOR(dff)
    {
        SC_CTHREAD(handle, clk.pos());
        reset_signal_is(rst, true);
    }

    void trace(sc_trace_file * tfp) const
    {
        sc_trace(tfp, clk, std::string(name()) + ".clk");
        sc_trace(tfp, rst, std::string(name()) + ".rst");
        sc_trace(tfp, ce, std::string(name()) + ".ce");
        sc_trace(tfp, d, std::string(name()) + ".d");
        sc_trace(tfp, q, std::string(name()) + ".q");
    }
};
// }
