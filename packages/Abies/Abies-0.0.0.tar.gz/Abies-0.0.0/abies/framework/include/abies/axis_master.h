#pragma once

#include "framework.h"
#include "axis.h"
#include <iostream>

namespace abies
{
    class AxisWriteIf : public virtual sc_core::sc_interface
    {
    public:
        virtual void write(uint32_t *data) = 0;
    };

    class AxisMaster : public AxisWriteIf, public sc_core::sc_module
    {
    public:
        sc_in_clk clk;
        sc_in<bool> rst;
        sc_out<uint32_t> tdata;
        sc_out<bool> tvalid;
        sc_in<bool> tready;

        // Non blocking write
        void handle()
        {
            wait();
            while (true)
            {

                if (rst)
                {
                    tvalid = 0;
                    std::cout << "AxisMaster reset" << std::endl;
                }
                else
                {
                    // Blocking write.
                    std::cout << "AxisMaster not reset" << std::endl;
                }
                wait();
            }
        }

        // void trace(sc_trace_file *tfp)
        // {
        //     std::cout << "Axis Master Enable Bus Tracing" << std::endl;
        //     sc_trace(tfp, clk, "clk");
        //     sc_trace(tfp, rst, "rst");
        //     sc_trace(tfp, tdata, "tdata");
        //     sc_trace(tfp, tvalid, "tvalid");
        //     sc_trace(tfp, tready, "tready");
        // }

        void write(uint32_t *data)
        {
            std::cout << "AxisMaster write: " << *data << std::endl;
        }

        SC_CTOR(AxisMaster)
        {
            SC_CTHREAD(handle, clk.pos());
            reset_signal_is(rst, true);
        }
    };
} // namespace abies
