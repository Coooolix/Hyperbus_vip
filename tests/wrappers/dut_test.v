`timescale 1ps/1ps

module hbram_ctrl_test(
);

  initial begin
      $dumpfile("dut.vcd");
      $dumpvars;
      CLK=0;
   forever begin
      #5 CLK=~CLK;
      end
   end
   endmodule
