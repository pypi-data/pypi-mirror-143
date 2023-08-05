// Flip flop with synchronous rst_n and ce.
module dff #(
    parameter DW = 24,
    parameter RST_VAL = 0
) (
    input  logic          clk,
    input  logic          rst,
    input  logic          ce,
    input  logic [DW-1:0] d,
    output logic [DW-1:0] q
);

  initial q = RST_VAL;

  always_ff @(posedge clk) begin
    if (rst) begin
      q <= RST_VAL;
    end else if (ce) begin
      q <= d;
    end
  end

endmodule
