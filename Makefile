SHELL=/bin/bash
CONDAROOT=/USER_SUPPLIED_DIRECTORY/miniconda3
PYENV=env

install:
	source $(CONDAROOT)/bin/activate && conda env create -f environment.yml
	# source $(CONDAROOT)/bin/activate && conda activate epimap-data && pip install git+git://github.com/epimap/covid19_datasets.git@master

preprocess-data:
	source $(CONDAROOT)/bin/activate && conda activate Rmap && pip install git+git://github.com/rs-delve/covid19_datasets.git@master
	source $(CONDAROOT)/bin/activate && conda activate Rmap && python process_uk_cases.py
	source $(CONDAROOT)/bin/activate && conda activate Rmap && python process_mobility.py
	source $(CONDAROOT)/bin/activate && conda activate Rmap && python process_metadata.py
	# source $(CONDAROOT)/bin/activate && conda activate Rmap && python process_site_data.py --output_dir "site_folder"
	source $(CONDAROOT)/bin/activate && conda activate Rmap && python group_local_authorities.py processed_data/traffic_flux_row-normed.csv processed_data/traffic_flux_transpose_row-normed.csv processed_data/areas.csv processed_data/region-groupings.json --threshold=0.8
	source $(CONDAROOT)/bin/activate && conda activate Rmap && python process_data.py
	source $(CONDAROOT)/bin/activate && conda activate Rmap && python traffic/create_traffic_matrix.py
	source $(CONDAROOT)/bin/activate && conda activate Rmap && python traffic/process_alt_traffic.py

environment-no-conda:
	# Only create the environment if it does not exist already.
	@if [ -d "$(PYENV)" ]; then\
	    python3 -m venv $(PYENV);\
	fi
	source $(PYENV)/bin/activate && pip install -r requirements.txt

preprocess-data-no-conda:
	source $(PYENV)/bin/activate && pip install git+git://github.com/rs-delve/covid19_datasets.git@master
	source $(PYENV)/bin/activate && python process_uk_cases.py
	source $(PYENV)/bin/activate && python process_mobility.py
	source $(PYENV)/bin/activate && python process_metadata.py
	# source $(PYENV)/bin/activate && python process_site_data.py --output_dir "site_folder"
	source $(PYENV)/bin/activate && python group_local_authorities.py processed_data/traffic_flux_row-normed.csv processed_data/traffic_flux_transpose_row-normed.csv processed_data/areas.csv processed_data/region-groupings.json --threshold=0.8
	source $(PYENV)/bin/activate && python process_data.py
	source $(PYENV)/bin/activate && python traffic/create_traffic_matrix.py
	source $(PYENV)/bin/activate && python traffic/process_alt_traffic.py
