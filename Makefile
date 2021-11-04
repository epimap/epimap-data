SHELL=/bin/bash
CONDAROOT=/USER_SUPPLIED_DIRECTORY/miniconda3

install:
	source $(CONDAROOT)/bin/activate && conda env create -f environment.yml
	# source $(CONDAROOT)/bin/activate && conda activate epimap-data && pip install git+git://github.com/epimap/covid19_datasets.git@master
	mkdir -p processed_data

preprocess-data:
	source $(CONDAROOT)/bin/activate && conda activate epimap-data && python process_uk_cases.py
	source $(CONDAROOT)/bin/activate && conda activate epimap-data && python process_mobility.py
	source $(CONDAROOT)/bin/activate && conda activate epimap-data && python process_metadata.py
	# source $(CONDAROOT)/bin/activate && conda activate epimap-data && python process_site_data.py --output_dir "site_folder"
	source $(CONDAROOT)/bin/activate && conda activate epimap-data && python process_data.py
	source $(CONDAROOT)/bin/activate && conda activate epimap-data && python traffic/create_traffic_matrix.py
	source $(CONDAROOT)/bin/activate && conda activate epimap-data && python traffic/process_alt_traffic.py
	# source $(CONDAROOT)/bin/activate && conda activate epimap-data && python traffic/process_real_traffic.py
	# source $(CONDAROOT)/bin/activate && conda activate epimap-data && python group_local_authorities.py processed_data/traffic_flux_row-normed.csv processed_data/traffic_flux_transpose_row-normed.csv processed_data/areas.csv processed_data/region-groupings.json --threshold=0.8
