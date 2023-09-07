import cocotb
from cocotb.result import TestFailure
from cocotb_coverage.coverage import CoverCross, CoverPoint, coverage_db
from cocotb.triggers import Timer
import os
from dut_init import test_dut_init
from dut_drivers import InputDriver, OutputDriver, ConfigDriver
from dut_monitor import IO_Monitor
import random

def scoreboard(transaction):
    """
    Scoreboard function to check that the transaction was received correctly.
    """
    expected_values = {
        "idle": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "rdy": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        "txn": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    }
    assert transaction["phase"] in expected_values.keys()
    for i in range(len(transaction["DQ"])):
        assert transaction["DQ"][i] == expected_values[transaction["phase"]][i]


@test(coverpoint=["transaction.phase"], covercross=[("transaction.phase", "transaction.CSNeg")])
async def test_dut(dut):
    """
    Testbench to verify the behavior of the Hyperbus HDL.
    """
    # Initialize clock
    clock = Clock(dut.CK, 5, units="ns")  # 200MHz
    cocotb.fork(clock.start())

    # Initialize signals
    await test_dut_init(dut)

    # Create bus monitor
    bus_monitor = IOMonitor(dut, "bus_monitor", clock)

    # Create input driver
    input_driver = InputDriver(dut, "input_driver", clock)

    # Create output driver
    output_driver = OutputDriver(dut, "output_driver", clock)

    # Generate random transactions
    while True:
        transaction = {
            "phase": cocotb.random.choice(["idle", "rdy", "txn"]),
            "CSNeg": cocotb.random.randint(0, 1),
            "CK": cocotb.random.randint(0, 1),
            "CKn": cocotb.random.randint(0, 1),
            "RESETNeg": cocotb.random.randint(0, 1),
            "RWDS": cocotb.random.randint(0, 1),
            "DQ7": cocotb.random.randint(0, 1),
            "DQ6": cocotb.random.randint(0, 1),
            "DQ5": cocotb.random.randint(0, 1),
            "DQ4": cocotb.random.randint(0, 1),
            "DQ3": cocotb.random.randint(0, 1),
            "DQ2": cocotb.random.randint(0, 1),
            "DQ1": cocotb.random.randint(0, 1),
            "DQ0": cocotb.random.randint(0, 1),
        }

        # Send the transaction
        input_driver.driver_send(transaction)

        # Wait for the transaction to be received
        await RisingEdge(dut.CK)

        # Check that the transaction was received correctly
        coverage.cover(transaction)
