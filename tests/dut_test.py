import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.result import TestFailure
from dut_init import dut_init
from dut_driver import IODriver, ConfigDriver
from dut_monitor import IOMonitor

@cocotb.coroutine
def scoreboard(driver, monitor):
    while True:
        yield RisingEdge(driver.clock)
        if len(driver.sent_transactions) != len(monitor.received_transactions):
            raise TestFailure("Number of sent and received transactions do not match")
        for i in range(len(driver.sent_transactions)):
            if driver.sent_transactions[i] != monitor.received_transactions[i]:
                raise TestFailure("Sent and received transactions do not match")

@cocotb.test()
async def test_dut(dut):
    dut_init(dut)

    clock = Clock(dut.clock, 10, units="ns")
    cocotb.fork(clock.start())

    io_driver = IODriver(dut, "io_driver", clock)
    config_driver = ConfigDriver(dut, "config_driver", clock)
    io_monitor = IOMonitor(dut, "io_monitor", clock)

    cocotb.fork(io_monitor.monitor_recv())

    await io_driver.driver_send({"CSNeg": 1, "CK": 0, "CKn": 1, "RESETNeg": 1})
    await config_driver.driver_send({"CSNeg": 1, "CK": 0, "CKn": 1, "RESETNeg": 1})

    await Timer(100, units="ns")

    await io_driver.driver_send({"CSNeg": 0, "CK": 0, "CKn": 1, "RESETNeg": 1, "DQ0": 1, "DQ1": 0, "DQ2": 1, "DQ3": 0})
    await io_driver.driver_send({"CSNeg": 0, "CK": 1, "CKn": 0, "RESETNeg": 1, "DQ0": 0, "DQ1": 1, "DQ2": 0, "DQ3": 1})
    await io_driver.driver_send({"CSNeg": 0, "CK": 0, "CKn": 1, "RESETNeg": 1, "DQ0": 1, "DQ1": 1, "DQ2": 0, "DQ3": 1})
    await io_driver.driver_send({"CSNeg": 1, "CK": 0, "CKn": 1, "RESETNeg": 1})

    await Timer(100, units="ns")

    await io_driver.driver_send({"CSNeg": 0, "CK": 0, "CKn": 1, "RESETNeg": 1, "DQ0": 0, "DQ1": 0, "DQ2": 0, "DQ3": 0})
    await io_driver.driver_send({"CSNeg": 0, "CK": 1, "CKn": 0, "RESETNeg": 1, "DQ0": 1, "DQ1": 1, "DQ2": 1, "DQ3": 1})
    await io_driver.driver_send({"CSNeg": 1, "CK": 0, "CKn": 1, "RESETNeg": 1})

    await Timer(100, units="ns")

    await io_driver.driver_send({"CSNeg": 0, "CK": 0, "CKn": 1, "RESETNeg": 1, "DQ0": 1, "DQ1": 1, "DQ2": 1, "DQ3": 0})
    await io_driver.driver_send({"CSNeg": 0, "CK": 1, "CKn": 0, "RESETNeg": 1, "DQ0": 0, "DQ1": 0, "DQ2": 1, "DQ3": 1})
    await io_driver.driver_send({"CSNeg": 1, "CK": 0, "CKn": 1, "RESETNeg": 1})

    await Timer(100, units="ns")

    await io_driver.driver_send({"CSNeg": 0, "CK": 0, "CKn": 1, "RESETNeg": 1, "DQ0": 0, "DQ1": 1, "DQ2": 1, "DQ3": 0})
   await io_driver.driver_send({"CSNeg": 0, "CK": 1, "CKn": 0, "RESETNeg": 1, "DQ0": 1, "DQ1": 0, "DQ2": 0, "DQ3": 1})
    await io_driver.driver_send({"CSNeg": 1, "CK": 0, "CKn": 1, "RESETNeg": 1})
