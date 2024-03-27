test:
	rm -rf output
	eachrundi
	bash -x output/all.sh
	docker run --rm -ti docker.io/taylorm/emeraldchanter:latest ./run_test.sh

clean:
	bash -x output/token_cleanup.sh
	rm -rf output
