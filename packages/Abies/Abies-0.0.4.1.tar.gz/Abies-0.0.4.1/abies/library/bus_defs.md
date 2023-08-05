# Signal Definitions

Modules must comply with naming and bus conventions.
Names must match exactly.

## Common Parameters
Modules may be required to implement these parameters.
Parameters should have defaults.

    parameter ADW = 24; // Audio bus data width
    parameter CDW = 8;  // Control bus data width
    parameter AW = 24;  // Address Width

## Common signals
All modules must have these signals in their port:

    input  logic clk;
    input  logic rst;

clk will be the processing clock. This is not the sample clock.
rst can be unused, but the rst port must be present to comply with code tools.

## Audio Bus Definition

Modules may have audio input and audio output ports.
The valid signal is the sample clock. There will be fclk/fsclk samples between each sample. 100e6 / 48e3 = 2083 for example. Audio modules can take no more clock cycles than this to process data.

Sometimes implementing ready is not necessary, or the developer may not want to implement stalling logic. So it is mostly optional. An audio sample clock is fairly slow and regular, so this shouldn't be a big deal.

Skid buffers can be used to connect modules that don't properly implement the ready signal. Use them if dropping data is a possibility. They are an easy way to automatically handle ready logic.

### Audio Input

    input  logic [DW-1:0] audio_i_data;
    input  logic audio_i_valid;
    output logic audio_i_ready;

If your design is fully pipelined or takes much fewer than fclk/sclk clock cycles to process data, you probably don't need to worry about the ready signal. You can "assign audio_i_ready = 1;" and everything will be fine.

If your design takes close to fclk/fsclk cycles, you should handle the ready signal properly. If you are unsure if the previous module in the chain is going to respect the ready signal, you can connect a skid buffer before your module to make sure you don't lose data.


### Audio Output
    output logic [DW-1:0] audio_o_data;
    output logic audio_o_valid;
    input  logic audio_o_ready;

If you can't stall or don't want to implement it, you can ignore the ready signal.