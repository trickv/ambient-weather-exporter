IMG_TAG=reedswenson/ambient-weather-exporter:latest
cur_dir:=$(shell pwd)

build: clean
	mkdir .build
	cp src/*.py src/*.yaml src/*.json src/*.txt .build
	cd .build && docker build . -f ../Dockerfile -t $(IMG_TAG)

clean:
	rm -rf .build

push:
	docker push $(IMG_TAG)

run_container:
	docker run --rm -it \
	-p 9000:9000 \
	-v $(cur_dir)/test:/app/config \
	$(IMG_TAG)