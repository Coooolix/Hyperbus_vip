SIM ?= icarus
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES += $(PWD)/../hdl/hbram_ctrl.v
VERILOG_SOURCES += $(PWD)/wrappers/dut_test.v
VERILOG_SOURCES += $(PWD)/../hdl/dut.v

dut:
	rm	-rf	sim_build
	$(MAKE)	sim	MODULE=dut_test	TOPLEVEL=dut_test
include	$(shell	cocotb-config	--makefiles)/Makefile.sim
