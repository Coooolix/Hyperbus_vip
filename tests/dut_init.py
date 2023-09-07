import cocotb
from cocotb.triggers import RisingEdge, Timer

async def dut_init(dut):
    # Initialize signals
    dut.CSNeg <= 1
    dut.CK <= 0
    dut.CKn <= 1
    dut.RESETNeg <= 0
    dut.DQ7 <= 0
    dut.DQ6 <= 0
    dut.DQ5 <= 0
    dut.DQ4 <= 0
    dut.DQ3 <= 0
    dut.DQ2 <= 0
    dut.DQ1 <= 0
    dut.DQ0 <= 0
    dut.RWDS <= 0

    # Apply reset signal
    dut.RESETNeg <= 1
    await Timer(10, units='ns')
    dut.RESETNeg <= 0
    await Timer(10, units='ns')
    dut.RESETNeg <= 1

    # Wait for reset to complete
    await RisingEdge(dut.CK)
    while dut.RESETNeg.value == 0:
        await RisingEdge(dut.CK)
    await Timer(1, units='us')
