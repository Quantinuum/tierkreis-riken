
docs:
	cd documentation && uv run sphinx-build -M html source build

stubs:
	cd scripts && uv run generate_stubs.py
	cd workers/tkr_qulacs && uv run main.py --stubs-path stubs.py
	cd workers/tkr_ibm_kobe && uv run main.py --stubs-path stubs.py
	cd workers/examples_worker && uv run main.py --stubs-path stubs.py

login:
	echo $$GH_REGISTRY_TOKEN | docker login ghcr.io -u mwpb --password-stdin


qulacs-worker:
	cd workers/tkr_qulacs && docker buildx build --platform linux/arm64/v8 -t qulacs-worker . --progress plain
	docker image tag qulacs-worker ghcr.io/quantinuum-dev/fugaku/qulacs-worker:latest
	docker push ghcr.io/quantinuum-dev/fugaku/qulacs-worker:latest

pull:
	singularity registry login --username mwpb docker://ghcr.io
	export SINGULARITY_TMPDIR=/tmp/tierkreis-singularity/
	mkdir -p /tmp/tierkreis-singularity
	singularity pull --force --arch arm64 docker://ghcr.io/quantinuum-dev/fugaku/qulacs-worker

run:
	singularity run docker://ghcr.io/quantinuum-dev/fugaku/qulacs-worker