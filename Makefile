SHELL=/bin/bash
CONDAROOT=/USER_SUPPLIED_DIRECTORY/miniconda3

install:
	virtualenv -p python3.8 venv
	source venv/bin/activate && pip install -r requirments.txt

preprocess-data:
	source venv/bin/activate && python process_uk_cases.py
	source venv/bin/activate && python process_mobility.py
	source venv/bin/activate && python process_metadata.py
	# source venv/bin/activate && python process_site_data.py --output_dir "site_folder"
	source venv/bin/activate && python group_local_authorities.py processed_data/traffic_flux_row-normed.csv processed_data/traffic_flux_transpose_row-normed.csv processed_data/areas.csv processed_data/region-groupings.json --threshold=0.8
	source venv/bin/activate && python process_data.py
	source venv/bin/activate && python traffic/create_traffic_matrix.py
	source venv/bin/activate && python traffic/process_alt_traffic.py
