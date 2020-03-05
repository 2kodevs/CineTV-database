.DEFAULT_GOAL 	:= help

# Project details
ORG_NAME 		:= 2kodevs
PROJECT_NAME 	:= CineTV-database
APP_VERSION		:= v0.1
APP_DESCRIPTION := $(ORG_NAME) - $(PROJECT_NAME)$(APP_VERSION)
DEVELOPERS		:= Lázaro Raúl Iglesias Vera, Miguel Tenorio Potrony, Carmen Irene Cabrera Rodríguez
COPYRIGHT	 	:= Copyright © 2020: $(DEVELOPERS)

MAIN_FOLDER		:= Files
PDF_PATH 		:= "$(MAIN_FOLDER)/pdf/"
DATA_PATH 		:= "$(MAIN_FOLDER)/data/"
DB_PATH 		:= "$(MAIN_FOLDER)/db/"

directories: ## Create project directories
	@mkdir -p $(DATA_PATH)
	@mkdir -p $(PDF_PATH)
	@mkdir -p $(DB_PATH)

download: directories ## Download data files
	@touch icultura.pdf
	@wget -P $(PDF_PATH) $(shell python downloader.py)
	@rm icultura.pdf

rename: directories ## Rename the downloaded files
	@python renamer.py -p $(PDF_PATH)

parse: directories ## Find ans save important pages
	@python page_filter.py -p $(PDF_PATH) -f $(DATA_PATH)

db: directories ## Build a database with the data
	@python data_parser.py -p $(DATA_PATH)

install: ## Install dependencies
	@pip install requierements.txt

help: ## Show this help
	@echo $(APP_DESCRIPTION)
	@echo Developed by: $(DEVELOPERS)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

