import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.binary import BinaryValue

@cocotb.test()
async def test_dut_init(dut):
    # Initialize clock
    clock = Clock(dut.CK, 5, units="ns")  # 200MHz
    cocotb.fork(clock.start())

    # Initialize signals
    dut.CSNeg <= 1
    dut.CK <= 0
    dut.CKn <= 1
    dut.RESETNeg <= 1
    dut.RWDS <= 0
    dut.DQ7 <= BinaryValue("zzzzzzzz")
    dut.DQ6 <= BinaryValue("zzzzzzzz")
    dut.DQ5 <= BinaryValue("zzzzzzzz")
    dut.DQ4 <= BinaryValue("zzzzzzzz")
    dut.DQ3 <= BinaryValue("zzzzzzzz")
    dut.DQ2 <= BinaryValue("zzzzzzzz")
    dut.DQ1 <= BinaryValue("zzzzzzzz")
    dut.DQ0 <= BinaryValue("zzzzzzzz")

    # Wait for a few clock cycles
    for i in range(10):
        await RisingEdge(dut.CK)

    # Assert RESETNeg
    dut.RESETNeg <= 0
    await Timer(10, units="ns")
    dut.RESETNeg <= 1

    # Deassert CSNeg
    dut.CSNeg <= 0
    await Timer(10, units="ns")
