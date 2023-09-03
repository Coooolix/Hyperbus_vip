module s27kl0642_test
    (
    DQ7      ,
    DQ6      ,
    DQ5      ,
    DQ4      ,
    DQ3      ,
    DQ2      ,
    DQ1      ,
    DQ0      ,
    RWDS     ,

    CSNeg    ,
    CK       ,
	CKn		 ,
    RESETNeg
    );
 inout  DQ7;
    inout  DQ6;
    inout  DQ5;
    inout  DQ4;
    inout  DQ3;
    inout  DQ2;
    inout  DQ1;
    inout  DQ0;
    inout  RWDS;

    input  CSNeg;
    input  CK;
	input  CKn;
    input  RESETNeg;

s27kl0642 u1(
	.DQ7(DQ7)      ,
	.DQ6(DQ6)      ,
	.DQ5(DQ5)      ,
	.DQ4(DQ4)      ,
	.DQ3(DQ3)      ,
	.DQ2(DQ2)      ,
	.DQ1(DQ1)      ,
	.DQ0(DQ0)      ,
	.RWDS(RWDS)     ,

	.CSNeg(CSNeg)    ,
	.CK(CK)       ,
	.CKn(CKn)		 ,
	.RESETNeg(RESETNeg)
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
