#pragma once

#include "framework.h"
#include <iostream>

namespace abies
{
    class AxisReadIf : public virtual sc_core::sc_interface
    {
        virtual void read(uint32_t *data) = 0;
    };

    class AxisSlave : public AxisReadIf, public sc_core::sc_module
    {
    public:
        sc_in_clk clk;
        sc_in<bool> rst;
        sc_in<uint32_t> tdata;
        sc_in<bool> tvalid;
        sc_out<bool> tready;

        // Non blocking write
        void handle()
        {
            wait();
            while (true)
            {
                if (rst)
                {
                    tready = 1;
                    std::cout << "AxisSlave reset" << std::endl;
                }
                else
                {
                    // Blocking write.
                    if (tvalid && tready)
                    {
                        std::cout << "AxisSlave Read transaction" << std::endl;
                    }
                }
                wait();
            }
        }

        void read(uint32_t *data)
        {
            std::cout << "AxisSlave read: " << tdata << std::endl;
            *data = tdata;
        }

        SC_CTOR(AxisSlave)
        {
            SC_CTHREAD(handle, clk.pos());
            reset_signal_is(rst, true);
        }
    };
} // namespace abies
