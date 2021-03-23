SHELL=/bin/bash
CONDAROOT=/data/ziz/mhutchin/miniconda3

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
