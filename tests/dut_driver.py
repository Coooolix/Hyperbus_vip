import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.binary import BinaryValue
from cocotb_bus.drivers import BusDriver

class InputDriver(BusDriver):
    _signals = ["CSNeg", "CK", "CKn", "RESETNeg"]
    _optional_signals = ["RWDS"]
    _data_signals = ["DQ7", "DQ6", "DQ5", "DQ4", "DQ3", "DQ2", "DQ1", "DQ0"]

    def __init__(self, entity, name, clock):
        BusDriver.__init__(self, entity, name, clock)
        self.bus.CSNeg.setimmediatevalue(1)
        self.bus.CK.setimmediatevalue(0)
        self.bus.CKn.setimmediatevalue(1)
        self.bus.RESETNeg.setimmediatevalue(1)
        if hasattr(self.bus, "RWDS"):
            self.bus.RWDS.setimmediatevalue(0)
        for signal in self._data_signals:
            getattr(self.bus, signal).setimmediatevalue(BinaryValue("zzzzzzzz"))

    async def driver_send(self, transaction, sync=True, **kwargs):
        if sync:
            await RisingEdge(self.clock)
        for signal in self._data_signals:
            getattr(self.bus, signal).append(transaction[signal])
        if hasattr(self.bus, "RWDS"):
            self.bus.RWDS.append(transaction["RWDS"])
        self.bus.CSNeg <= 0
        await RisingEdge(self.clock)
        self.bus.CK <= 1
        self.bus.CKn <= 0
        await RisingEdge(self.clock)
        self.bus.CK <= 0
        self.bus.CKn <= 1
        await RisingEdge(self.clock)
        self.bus.CSNeg <= 1
        if "callback" in kwargs:
            kwargs["callback"]()

class OutputDriver(BusDriver):
    _signals = ["CSNeg", "CK", "CKn", "RESETNeg"]
    _optional_signals = ["RWDS"]
    _data_width = 8

    def __init__(self, entity, name, clock):
        BusDriver.__init__(self, entity, name, clock)
        self.bus.CSNeg.setimmediatevalue(1)
        self.bus.CK.setimmediatevalue(0)
        self.bus.CKn.setimmediatevalue(1)
        self.bus.RESETNeg.setimmediatevalue(1)
        if hasattr(self.bus, "RWDS"):
            self.bus.RWDS.setimmediatevalue(0)

    async def driver_send(self, transaction, sync=True, **kwargs):
        if sync:
            await RisingEdge(self.clock)
        self.bus.CSNeg <= 0
        await RisingEdge(self.clock)
        self.bus.CK <= 1
        self.bus.CKn <= 0
        await RisingEdge(self.clock)
        if hasattr(self.bus, "RWDS"):
            transaction["RWDS"] = self.bus.RWDS.value
        for i in range(self.data_width):
            transaction["DQ{}".format(i)] = self.bus.DQ[i].value
        self.bus.CK <= 0
        self.bus.CKn <= 1
        await RisingEdge(self.clock)
        self.bus.CSNeg <= 1
        if "callback" in kwargs:
            kwargs["callback"]()

class ConfigDriver(BusDriver):
    _signals = ["CSNeg", "CK", "CKn", "RESETNeg"]
    _data_signals = ["DQ7", "DQ6", "DQ5", "DQ4", "DQ3", "DQ2", "DQ1", "DQ0"]

    def __init__(self, entity, name, clock):
        BusDriver.__init__(self, entity, name, clock)
        self.bus.CSNeg.setimmediatevalue(1)
        self.bus.CK.setimmediatevalue(0)
        self.bus.CKn.setimmediatevalue(1)
        self.bus.RESETNeg.setimmediatevalue(1)
        for signal in self._data_signals:
            getattr(self.bus, signal).setimmediatevalue(BinaryValue("zzzzzzzz"))

    async def driver_send(self, transaction, sync=True, **kwargs):
        if sync:
            await RisingEdge(self.clock)
        for signal in self._data_signals:
            getattr(self.bus, signal).append(transaction[signal])
        self.bus.CSNeg <= 0
        await RisingEdge(self.clock)
        self.bus.CK <= 1
        self.bus.CKn <= 0
        await RisingEdge(self.clock)
        self.bus.CK <= 0
        self.bus.CKn <= 1
        await RisingEdge(self.clock)
        self.bus.CSNeg <= 1
        if "callback" in kwargs:
            kwargs["callback"]()
