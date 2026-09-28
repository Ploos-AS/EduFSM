PYTHON ?= python3
BUILD := build
MODULE := turnstile
PCF := upduino_v31.pcf

.PHONY: generate test bitstream clean

generate:
	mkdir -p $(BUILD)
	edufsm hdl ../../examples/turnstile.fsm --target systemverilog --module $(MODULE) > $(BUILD)/$(MODULE).sv
	edufsm hdl ../../examples/turnstile.fsm --target testbench --module $(MODULE) > $(BUILD)/$(MODULE)_tb.sv

test: generate
	iverilog -g2012 -s $(MODULE)_tb -o $(BUILD)/$(MODULE).vvp $(BUILD)/$(MODULE).sv $(BUILD)/$(MODULE)_tb.sv
	vvp $(BUILD)/$(MODULE).vvp

bitstream: generate
	yosys -p 'read_verilog -sv $(BUILD)/$(MODULE).sv; synth_ice40 -top $(MODULE) -json $(BUILD)/$(MODULE).json'
	nextpnr-ice40 --up5k --package sg48 --json $(BUILD)/$(MODULE).json --pcf $(PCF) --asc $(BUILD)/$(MODULE).asc --freq 12
	icepack $(BUILD)/$(MODULE).asc $(BUILD)/$(MODULE).bin

clean:
	rm -rf $(BUILD)
