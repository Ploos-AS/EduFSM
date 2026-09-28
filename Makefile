PYTHON ?= python3
PANDOC ?= pandoc
BUILD := build
LANGS := no en

.PHONY: all clean diagrams sources exercises html epub kindle pdf

all: html epub kindle pdf

diagrams:
	@mkdir -p $(BUILD)/diagrams
	@PYTHONPATH=. $(PYTHON) scripts/build_diagrams.py

sources: diagrams
	@mkdir -p $(BUILD)
	@for lang in $(LANGS); do $(PYTHON) scripts/build_book.py $$lang $(BUILD)/edufsm-$$lang.md; done

exercises:
	@mkdir -p $(BUILD)
	@for lang in $(LANGS); do PYTHONPATH=scripts $(PYTHON) scripts/build_exercises.py $$lang $(BUILD)/exercises-$$lang.md; done

html: sources exercises
	@for lang in $(LANGS); do mkdir -p $(BUILD)/site/$$lang; $(PANDOC) $(BUILD)/edufsm-$$lang.md --resource-path=$(BUILD) --standalone --toc --metadata title="EduFSM" -o $(BUILD)/site/$$lang/index.html; $(PANDOC) $(BUILD)/exercises-$$lang.md --standalone --toc --metadata title="EduFSM Exercises" -o $(BUILD)/site/$$lang/exercises.html; done

epub: sources exercises
	@for lang in $(LANGS); do $(PANDOC) $(BUILD)/edufsm-$$lang.md --resource-path=$(BUILD) --toc --metadata title="EduFSM" --metadata lang=$$lang -o $(BUILD)/edufsm-$$lang.epub; $(PANDOC) $(BUILD)/exercises-$$lang.md --toc --metadata title="EduFSM Exercises" --metadata lang=$$lang -o $(BUILD)/edufsm-exercises-$$lang.epub; done

kindle: sources
	@for lang in $(LANGS); do $(PANDOC) $(BUILD)/edufsm-$$lang.md --resource-path=$(BUILD) --toc --metadata title="EduFSM" --metadata lang=$$lang -o $(BUILD)/edufsm-$$lang-kindle.epub; done

pdf: sources exercises
	@for lang in $(LANGS); do $(PANDOC) $(BUILD)/edufsm-$$lang.md --resource-path=$(BUILD) --toc --pdf-engine=xelatex --variable=geometry:margin=25mm --variable=mainfont="DejaVu Sans" --variable=monofont="DejaVu Sans Mono" -o $(BUILD)/edufsm-$$lang.pdf; $(PANDOC) $(BUILD)/exercises-$$lang.md --toc --pdf-engine=xelatex --variable=geometry:margin=25mm --variable=mainfont="DejaVu Sans" --variable=monofont="DejaVu Sans Mono" -o $(BUILD)/edufsm-exercises-$$lang.pdf; done

clean:
	rm -rf $(BUILD)
