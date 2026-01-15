
docs:
	cd documentation && uv run sphinx-build -M html source build

stubs:
	cd scripts && uv run generate_stubs.py
	cd workers/tkr_ibm_kobe && uv run main.py --stubs-path stubs.py
	cd workers/tkr_reimei && uv run main.py --stubs-path stubs.py
