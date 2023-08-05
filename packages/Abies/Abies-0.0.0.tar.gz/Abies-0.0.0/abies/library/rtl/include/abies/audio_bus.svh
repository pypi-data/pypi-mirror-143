`ifndef AUDIO_BUS_H
`define AUDIO_BUS_H

interface audio_bus;
  logic clk;
  logic rst;
  logic audio_data_i;
  logic audio_valid_i;
  logic audio_ready_o;
  logic audio_data_o;
  logic audio_valid_o;
  logic audio_ready_i;

endinterface

`endif
