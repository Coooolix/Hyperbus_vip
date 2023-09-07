import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def dut_init(dut):
    # Initialize all input signals
    dut.CSNeg <= 1
    dut.CK <= 0
    dut.CKn <= 1
    dut.RESETNeg <= 1

    # Initialize all output signals
    dut.DQ7 <= 0
    dut.DQ6 <= 0
    dut.DQ5 <= 0
    dut.DQ4 <= 0
    dut.DQ3 <= 0
    dut.DQ2 <= 0
    dut.DQ1 <= 0
    dut.DQ0 <= 0
    dut.RWDS <= 0

    # Wait for a few clock cycles
    for i in range(5):
        await RisingEdge(dut.CK)
        await FallingEdge(dut.CK)

    # Assert RESETNeg signal
    dut.RESETNeg <= 0
    await Timer(10, units='ns')
    dut.RESETNeg <= 1

    # Wait for a few clock cycles
    for i in range(5):
        await RisingEdge(dut.CK)
        await FallingEdge(dut.CK)

    # Assert CSNeg signal
    dut.CSNeg <= 0
    await Timer(10, units='ns')
    dut.CSNeg <= 1

    # Wait for a few clock cycles
    for i in range(5):
        await RisingEdge(dut.CK)
        await FallingEdge(dut.CK)
