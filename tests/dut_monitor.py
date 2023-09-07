import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb_bus.monitors import BusMonitor

class IOMonitor(BusMonitor):
    _signals = ["CSNeg", "CK", "CKn", "RESETNeg"]
    _optional_signals = ["RWDS"]
    _data_signals = ["DQ7", "DQ6", "DQ5", "DQ4", "DQ3", "DQ2", "DQ1", "DQ0"]

    def __init__(self, entity, name, clock):
        BusMonitor.__init__(self, entity, name, clock)
        self.received_transactions = []

    async def _monitor_recv(self):
        while True:
            await RisingEdge(self.clock)
            transaction = {}
            transaction["CSNeg"] = int(self.bus.CSNeg.value)
            transaction["CK"] = int(self.bus.CK.value)
            transaction["CKn"] = int(self.bus.CKn.value)
            transaction["RESETNeg"] = int(self.bus.RESETNeg.value)
            if hasattr(self.bus, "RWDS"):
                transaction["RWDS"] = int(self.bus.RWDS.value)
            for i in range(len(self._data_signals)):
                transaction[self._data_signals[i]] = int(self.bus.DQ[i].value)
            self.received_transactions.append(transaction)
