install:
	pip install --upgrade -e .

conda_upgrade:
	conda env update -n gSSURGO -f environment.yml
