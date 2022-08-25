AMBIENT_API_KEY?=815f9c20cb7246f8bfb697aec0f1fdabb90a42123ccc4e999aefe13cbf707da0
AMBIENT_APPLICATION_KEY?=67a05cffa31946ad9f15ffbc0cbecdcf2e933d488eaa49ef84c8d40f566a0bcb

build:
	docker build . -t reedswenson/ambient-weather-exporter:latest

run_container:
	docker run --rm \
	-e AMBIENT_API_KEY=$(AMBIENT_API_KEY) \
	-e AMBIENT_APPLICATION_KEY=$(AMBIENT_APPLICATION_KEY) \
	-p 8000:8000 \
	reedswenson/ambient-weather-exporter:latest