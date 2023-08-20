from cocotb.drivers import BusDriver
from cocotb.triggers import RisingEdge

class InputBusDriver(BusDriver):
    def __init__(self, clk, reset, read, write, pause, delay=0):
        super().__init__(clk, reset)
        self.read = read
        self.write = write
        self.pause = pause
        self.delay = delay

    async def update(self):
        if RisingEdge(self.clk):
            if not self.reset:
                if self.read:
                    await self.read.trigger(delay=self.delay)
                if self.write:
                    await self.write.trigger(delay=self.delay)
                if self.pause:
                    await self.pause.trigger(delay=self.delay)

class OutputBusDriver(BusDriver):
    def __init__(self, clk, reset, data, delay=0):
        super().__init__(clk, reset)
        self.data = data
        self.delay = delay

    async def update(self):
        if RisingEdge(self.clk):
            if not self.reset:
                await self.data.write(delay=self.delay)

class ConfigurationBusDriver(BusDriver):
    def __init__(self, clk, reset, address, data, write, delay=0):
        super().__init__(clk, reset)
        self.address = address
        self.data = data
        self.write = write
        self.delay = delay

    async def update(self):
        if RisingEdge(self.clk):
            if not self.reset:
                await self.address.write(delay=self.delay)
                await self.data.write(delay=self.delay)
                await self.write.write(delay=self.delay)



class IO_Monitor(BusMonitor):
    def __init__(self, clk, reset, data, address, write, pause):
        super().__init__(clk, reset, data, address, write, pause)
        self.data_recv = []
        self.address_recv = []
        self.write_recv = []
        self.pause_recv = []
        self.transaction_states = {
            "IDLE": 0,
            "READ": 1,
            "WRITE": 2,
            "PAUSE": 3
        }

    async def update(self):
        if RisingEdge(self.clk):
            if not self.reset:
                if self.write.value:
                    self.transaction_states["WRITE"] += 1
                else:
                    self.transaction_states["READ"] += 1
                self.data_recv.append(self.data.value)
                self.address_recv.append(self.address.value)
                self.write_recv.append(self.write.value)
                self.pause_recv.append(self.pause.value)
