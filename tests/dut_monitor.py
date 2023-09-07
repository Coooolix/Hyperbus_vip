import cocotb
from cocotb.monitors import BusMonitor

class IOMonitor(BusMonitor):
    def __init__(self, dut, clock, reset):
        self.clock = clock
        self.reset = reset
        BusMonitor.__init__(self, dut, None, dut.clock)
        self.phase = "idle"

    async def monitor_recv(self):
        while True:
            await RisingEdge(self.clock)
            if self.phase == "idle":
                if self.bus.CSNeg.value == 0:
                    self.phase = "rdy"
            elif self.phase == "rdy":
                if self.bus.CSNeg.value == 1:
                    self.phase = "idle"
                elif self.bus.RWDS.value == 1:
                    self.phase = "txn"
                    data = [self.bus.DQ7.value, self.bus.DQ6.value, self.bus.DQ5.value, self.bus.DQ4.value,
                            self.bus.DQ3.value, self.bus.DQ2.value, self.bus.DQ1.value, self.bus.DQ0.value]
                    self._recv(data)
            elif self.phase == "txn":
                if self.bus.CSNeg.value == 1:
                    self.phase = "idle"
                elif self.bus.RWDS.value == 0:
                    self.phase = "rdy"
            await FallingEdge(self.clock)
