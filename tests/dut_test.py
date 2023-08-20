import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.drivers import BusDriver
from cocotb.coverage import CoverPoint, CoverCross
from cocotb.monitors import BusMonitor


class HBMController(object):
    def __init__(self, dut):
        self.dut = dut
        self.sys_clk = dut.sys_clk
        self.hb_clk = dut.hb_clk
        self.rwds = dut.rwds
        self.buffer = [0] * 1024
        self.read_buffer = [0] * 1024
        self.count = 0
        self.start = 0
        self.start_clk = 0
        self.CSNeg_tmp = 1
        self.sys_clk_period = 500
        self.period_cnt = freq / sys_clk_period
        self.pause = 0
        self.pause_count = 0
        self.rwds_sel = 0
        self.rwds_tmp = 0
        self.latency = 6
        self.reset_neg = 1
        self.rwds_in = 0

        self.driver = BusDriver(dut, "Dout", self.sys_clk)
        self.monitor = BusMonitor(dut, "Dout", self.sys_clk)

        @cocotb.coroutine
        def reset_sequence():
            yield RisingEdge(self.sys_clk)
            yield self.dut.reset_neg.eq(1)
            yield RisingEdge(self.sys_clk)
            yield self.dut.reset_neg.eq(0)
            yield RisingEdge(self.sys_clk)

        @cocotb.coroutine
        def test_sequence():
            while True:
                yield RisingEdge(self.start)
                cp_data = CoverPoint(self.driver.recv(), bins=range(256))
                cp_data.sample()
                yield RisingEdge(self.sys_clk)
                self.count = self.count + 1
                if self.count == end_count:
                    self.start = 0

        @cocotb.coroutine
        def input_driver():
            while True:
                yield RisingEdge(self.sys_clk)
                yield self.driver.send(self.buffer[self.count])
                yield RisingEdge(self.sys_clk)
                self.count = self.count + 1
                if self.count == end_count:
                    self.start = 0

        @cocotb.coroutine
        def output_driver():
            while True:
                yield RisingEdge(self.start)
                yield self.driver.send(self.buffer[self.count])
                yield RisingEdge(self.sys_clk)
                self.count = self.count + 1
                if self.count == end_count:
                    self.start = 0

        @cocotb.coroutine
        def config_driver():
            while True:
                yield RisingEdge(self.sys_clk)
                yield self.driver.send(self.buffer[self.count])
                yield RisingEdge(self.sys_clk)
                self.count = self.count + 1
                if self.count == end_count:
                    self.start = 0

        @cocotb.coroutine
        def io_monitor():
            while True:
                yield RisingEdge(self.sys_clk)
                yield self.monitor.recv()

        cocotb.run_until(reset_sequence())
        cocotb.fork(test_sequence())
        cocotb.fork(input_driver())
        cocotb.fork(output_driver())
        cocotb.fork(config_driver())
        cocotb.fork(io_monitor())
