PYTHON ?= python3
PANDOC ?= pandoc
BUILD := build
LANGS := no en

.PHONY: all clean diagrams sources html epub kindle pdf

all: html epub kindle pdf

diagrams:
	@mkdir -p $(BUILD)/diagrams
	@PYTHONPATH=. $(PYTHON) scripts/build_diagrams.py

sources: diagrams
	@mkdir -p $(BUILD)
	@for lang in $(LANGS); do $(PYTHON) scripts/build_book.py $$lang $(BUILD)/edufsm-$$lang.md; done

html: sources
	@for lang in $(LANGS); do mkdir -p $(BUILD)/site/$$lang; $(PANDOC) $(BUILD)/edufsm-$$lang.md --resource-path=$(BUILD) --standalone --toc --metadata title="EduFSM" -o $(BUILD)/site/$$lang/index.html; done

epub: sources
	@for lang in $(LANGS); do $(PANDOC) $(BUILD)/edufsm-$$lang.md --resource-path=$(BUILD) --toc --metadata title="EduFSM" --metadata lang=$$lang -o $(BUILD)/edufsm-$$lang.epub; done

kindle: sources
	@for lang in $(LANGS); do $(PANDOC) $(BUILD)/edufsm-$$lang.md --resource-path=$(BUILD) --toc --metadata title="EduFSM" --metadata lang=$$lang -o $(BUILD)/edufsm-$$lang-kindle.epub; done

pdf: sources
	@for lang in $(LANGS); do $(PANDOC) $(BUILD)/edufsm-$$lang.md --resource-path=$(BUILD) --toc --pdf-engine=xelatex --variable=geometry:margin=25mm --variable=mainfont="DejaVu Sans" --variable=monofont="DejaVu Sans Mono" -o $(BUILD)/edufsm-$$lang.pdf; done

clean:
	rm -rf $(BUILD)
