test:
	rm -rf output
	eachrundi
	cp output/README.md README.md
	bash -x output/all.sh
	docker run --rm -ti emeraldchanter:latest ./run_test.sh

pretty:
	ruff check --fix
	ruff format

readme:
	eachrundi
	cp output/README.md README.md

clean:
	bash -x output/token_cleanup.sh
	rm -rf output
