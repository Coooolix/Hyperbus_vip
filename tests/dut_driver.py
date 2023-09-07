import cocotb
from cocotb.drivers import BusDriver
from cocotb.triggers import RisingEdge, FallingEdge, Timer

class InputDriver(BusDriver):
    def __init__(self, dut, clock, reset):
        self.clock = clock
        self.reset = reset
        BusDriver.__init__(self, dut, None, dut.clock)

    async def send(self, data):
        self.bus.DQ7 <= data[7]
        self.bus.DQ6 <= data[6]
        self.bus.DQ5 <= data[5]
        self.bus.DQ4 <= data[4]
        self.bus.DQ3 <= data[3]
        self.bus.DQ2 <= data[2]
        self.bus.DQ1 <= data[1]
        self.bus.DQ0 <= data[0]
        await RisingEdge(self.clock)

class OutputDriver(BusDriver):
    def __init__(self, dut, clock, reset):
        self.clock = clock
        self.reset = reset
        self.queue = []
        BusDriver.__init__(self, dut, None, dut.clock)

    async def send(self, data):
        self.queue.append(data)

    async def append(self, data):
        self.queue.append(data)

    async def callback(self):
        while len(self.queue) > 0:
            data = self.queue.pop(0)
            self.bus.DQ7 <= data[7]
            self.bus.DQ6 <= data[6]
            self.bus.DQ5 <= data[5]
            self.bus.DQ4 <= data[4]
            self.bus.DQ3 <= data[3]
            self.bus.DQ2 <= data[2]
            self.bus.DQ1 <= data[1]
            self.bus.DQ0 <= data[0]
            self.bus.RWDS <= 1
            await RisingEdge(self.clock)
            self.bus.RWDS <= 0
            await RisingEdge(self.clock)

class ConfigDriver(BusDriver):
    def __init__(self, dut, clock, reset):
        self.clock = clock
        self.reset = reset
        BusDriver.__init__(self, dut, None, dut.clock)

    async def send(self, data):
        self.bus.CSNeg <= 0
        self.bus.DQ7 <= data[7]
        self.bus.DQ6 <= data[6]
        self.bus.DQ5 <= data[5]
        self.bus.DQ4 <= data[4]
        self.bus.DQ3 <= data[3]
        self.bus.DQ2 <= data[2]
        self.bus.DQ1 <= data[1]
        self.bus.DQ0 <= data[0]
        await RisingEdge(self.clock)
        self.bus.CSNeg <= 1
        await RisingEdge(self.clock)

class BusDriver(BusDriver):
    def __init__(self, dut, name, clock):
        self.clock = clock
        BusDriver.__init__(self, dut, name, clock)

    async def send(self, data):
        raise NotImplementedError("send method not implemented")
