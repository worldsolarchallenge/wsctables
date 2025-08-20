DOCKER_NAME=wsctables
DOCKER_TAG=latest
DOCKER_REPO=dcasnowdon

INFLUX_URL ?= "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_ORG ?= "Bridgestone World Solar Challenge"
INFLUX_BUCKET ?= test

#GOOGLEMAPS_KEY ?= AIzaSyD4cxmf6zr3SMovEYgZZe9eoEQCglqz3L8
ENV_VARS=INFLUX_TOKEN_TARGET CREDS_PATH CONFIG_YAML
#export $(ENV_VARS)

.PHONY: build run

all: run

build:
	docker build -t $(DOCKER_NAME):$(DOCKER_TAG) .

run: build
	docker run -p 5000:5000 $(foreach e,$(ENV_VARS),-e $(e)) $(DOCKER_NAME)

publish: build
	docker image tag $(DOCKER_NAME):$(DOCKER_TAG) $(DOCKER_REPO)/$(DOCKER_NAME):$(DOCKER_TAG)

build/testenv: pyproject.toml
		mkdir -p build && \
		python3 -m venv build/testenv && \
		build/testenv/bin/pip install -e ./deps/wsctools && \
		build/testenv/bin/pip install -e . && \
		touch $@

localtest: build/testenv
		. $</bin/activate && \
			INFLUX_TOKEN_TARGET=$$(cat ../wsc_spot_poll/wsc_bucket_token.key) \
			CREDS_PATH=$(HOME)/secret/wsctables-credentials.json \
			CONFIG_YAML=../config-test.yaml \
			flask --debug --app wsctables run

lint: build/testenv
		source $</bin/activate && \
				pip install pylint pylibmc && \
				pylint $$(git ls-files '*.py')

clean:
	rm -rf build
