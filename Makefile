.DEFAULT_GOAL 	:= help

# Project details
ORG_NAME 		:= 2kodevs
PROJECT_NAME 	:= CineTV-database
APP_VERSION		:= v0.1
APP_DESCRIPTION := $(ORG_NAME) - $(PROJECT_NAME)$(APP_VERSION)
DEVELOPERS		:= Lázaro Raúl Iglesias Vera, Miguel Tenorio Potrony, Carmen Irene Cabrera Rodríguez
COPYRIGHT	 	:= Copyright © 2020: $(DEVELOPERS)

DATA_PATH 		:= Cartelera JR 2019

download: ## Download data files
	@wget -P "$(DATA_PATH)" $(shell python downloader.py)

rename: ## Rename the downloaded files
	@python renamer.py

parse: ## Find ans save important pages
	@python page_filter.py

help: ## Show this help
	@echo $(APP_DESCRIPTION)
	@echo Developed by: $(DEVELOPERS)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

