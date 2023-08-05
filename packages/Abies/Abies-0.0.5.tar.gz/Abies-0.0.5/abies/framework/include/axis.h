#pragma once

#include <systemc.h>

namespace abies
{
    class Axis : public virtual sc_core::sc_interface
    {
        virtual void read(uint32_t *data) = 0;
        virtual void write(uint32_t *data) = 0;
    };
} // namespace abies
