import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep, FallingEdge
from cocotb_bus.drivers import BusDriver
from cocotb_coverage.coverage import CoverCross, CoverPoint, coverage_db
from cocotb_bus.monitors import BusMonitor
import os
import random

async def reset_dut(s27kl0642):
    s27kl0642.RESETNeg.value <= 0
    yield Timer(10, units="ns")
    s27kl0642.RESETNeg <= 1
    yield Timer(10, units="ns")

async def hyperbus_init(s27kl0642):
    # Set all signals to their initial values
    s27kl0642.DQ7 <= 0
    s27kl0642.DQ6 <= 0
    s27kl0642.DQ5 <= 0
    s27kl0642.DQ4 <= 0
    s27kl0642.DQ3 <= 0
    s27kl0642.DQ2 <= 0
    s27kl0642.DQ1 <= 0
    s27kl0642.DQ0 <= 0
    s27kl0642.RWDS <= 0
    s27kl0642.CSNeg <= 1
    s27kl0642.CK <= 0
    s27kl0642.CKn <= 1
    s27kl0642.RESETNeg <= 1

    # Send reset command
    await hyperbus_write(s27kl0642, 0xF0, 0x00, [])

    # Wait for initialization to complete
    await Timer(100, units='ns')

    # Set CSNeg low
    s27kl0642.CSNeg <= 0

@cocotb.test()
async def test_s27kl0642(s27kl0642):
    # Initialize clock
    clock = Clock(s27kl0642.ck, 10, units="ns")
    cocotb.fork(clock.start())

    # Initialize monitor
    monitor = HyperBusIOMonitor(s27kl0642, "HyperBusIOMonitor", clock)
    await monitor.start()
     cp_data = CoverPoint("cp_data", "Data coverage", bins=[0x0000, 0x1234, 0x5678, 0x9ABC, 0xFFFF])
    cp_rw = CoverPoint("cp_rw", "Read/Write coverage", bins=["Read", "Write"])
    cc_rw_data = CoverCross("cc_rw_data", "Read/Write vs. Data coverage", [cp_rw, cp_data])

    # Perform read transaction
    s27kl0642.cs <= 0
    s27kl0642.rw <= 1
    s27kl0642.address <= 0
    await RisingEdge(s27kl0642.ck)
    s27kl0642.data <= 0x1234
    await FallingEdge(s27kl0642.ck)
    s27kl0642.data <= 0x5678
    await FallingEdge(s27kl0642.ck)
    s27kl0642.data <= 0x9ABC
    await FallingEdge(s27kl0642.ck)
    s27kl0642.cs <= 1
 
# Record coverage for read transaction
    for data, rw in monitor.received_data:
        cp_data.hit(data)
        cp_rw.hit(rw)
        cc_rw_data.hit((rw, data))


    # Verify read transaction
    expected_data = [(0x1234, "Read"), (0x5678, "Read"), (0x9ABC, "Idle")]
    if monitor.received_data != expected_data:
        raise TestFailure("Received data does not match expected data")

    # Perform write transaction
    s27kl0642.cs <= 0
    s27kl0642.rw <= 0
    s27kl0642.address <= 0
    await RisingEdge(s27kl0642.ck)
    s27kl0642.data <= 0x4321
    await FallingEdge(s27kl0642.ck)
    s27kl0642.data <= 0x8765
    await FallingEdge(s27kl0642.ck)
    s27kl0642.data <= 0xCBA9
    await FallingEdge(s27kl0642.ck)
    s27kl0642.cs <= 1
 # Record coverage for write transaction
    for data, rw in monitor.received_data:
        cp_data.hit(data)
        cp_rw.hit(rw)
        cc_rw_data.hit((rw, data))

    # Verify coverage
    if cp_data.bins[0x0000].hits != 1:
        raise TestFailure("Data bin 0x0000 not hit")
    if cp_data.bins[0x1234].hits != 1:
        raise TestFailure("Data bin 0x1234 not hit")
    if cp_data.bins[0x5678].hits != 1:
        raise TestFailure("Data bin 0x5678 not hit")
    if cp_data.bins[0x9ABC].hits != 1:
        raise TestFailure("Data bin 0x9ABC not hit")
    if cp_data.bins[0xFFFF].hits != 3:
        raise TestFailure("Data bin 0xFFFF not hit 3 times")
    if cp_rw.bins["Read"].hits != 3:
        raise TestFailure("Read bin not hit 3 times")
    if cp_rw.bins["Write"].hits != 3:
        raise TestFailure("Write bin not hit 3 times")
    if cc_rw_data.cross_bins[("Read", 0x1234)].hits != 1:
        raise TestFailure("Read/0x1234 cross bin not hit")
    if cc_rw_data.cross_bins[("Read", 0x5678)].hits != 1:
        raise TestFailure("Read/0x5678 cross bin not hit")
    if cc_rw_data.cross_bins[("Read", 0x9ABC)].hits != 1:
        raise TestFailure("Read/0x9ABC cross bin not hit")
    if cc_rw_data.cross_bins[("Write", 0x4321)].hits != 1:
        raise TestFailure("Write/0x4321  cross bin not hit")
    if cc_rw_data.cross_bins[("Write", 0x8765)].hits != 1:
        raise TestFailure("Write/0x8765 cross bin not hit")
    if cc_rw_data.cross_bins[("Write", 0xCBA9)].hits != 1:
        raise TestFailure("Write/0xCBA9 cross bin not hit")


    # Verify write transaction
    expected_data = [(0, "Write"), (0, "Write"), (0, "Idle")]
    if monitor.received_data != expected_data:
        raise TestFailure("Received data does not match expected data")

def match_output(ref_output, dut_output):
    if len(ref_output) != len(dut_output):
        return False
    for i in range(len(ref_output)):
        if ref_output[i] != dut_output[i]:
            return False
    return True

class HyperBusOutputDriver(BusDriver):
    _signals = ["data", "address", "rw", "cs", "ck", "reset"]

    def __init__(self, entity, name, clock):
        BusDriver.__init__(self, entity, name, clock)
        self.bus.reset <= 1

    @cocotb.coroutine
    def write(self, data, address, rw, cs):
        self.bus.data <= data
        self.bus.address <= address
        self.bus.rw <= rw
        self.bus.cs <= cs
        self.bus.ck <= 0
        self.bus.reset <= 0
        yield RisingEdge(self.clock)
        self.bus.ck <= 1
        yield RisingEdge(self.clock)
        self.bus.ck <= 0
        yield RisingEdge(self.clock)
        self.bus.reset <= 1

class HyperBusInputDriver(BusDriver):
    _signals = ["data", "address", "rw", "cs", "ck", "reset"]

    def __init__(self, entity, name, clock):
        BusDriver.__init__(self, entity, name, clock)
        self.bus.reset <= 1

    @cocotb.coroutine
    def read(self, address, cs):
        self.bus.address <= address
        self.bus.rw <= 1
        self.bus.cs <= cs
        self.bus.ck <= 0
        self.bus.reset <= 0
        yield RisingEdge(self.clock)
        self.bus.ck <= 1
        yield RisingEdge(self.clock)
        data = self.bus.data.value.integer
        self.bus.ck <= 0
        yield RisingEdge(self.clock)
        self.bus.reset <= 1
        return data
        
class HyperBusIOMonitor(BusMonitor):
    _signals = ["data", "cs", "ck", "rw", "address"]

    def __init__(self, entity, name, clock):
        BusMonitor.__init__(self, entity, name, clock)
        self.received_data = []
        self.state = "Idle"

    @cocotb.coroutine
    def _monitor_recv(self):
        while True:
            yield RisingEdge(self.clock)
            if self.bus.cs.value.integer == 0:
                if self.bus.rw.value.integer == 1:
                    if self.bus.address.value.integer == 0:
                        self.state = "Read"
                    else:
                        self.state = "Read with Initial Latency"
                else:
                    if self.bus.address.value.integer == 0:
                        self.state = "Write"
                    else:
                        self.state = "Write with Initial Latency"
                data = self.bus.data.value.integer
                self.received_data.append((data, self.state))
                yield Timer(0.5)
            else:
                if self.bus.rw.value.integer == 1:
                    self.state = "Interrupt"
                else:
                    self.state = "Idle"
