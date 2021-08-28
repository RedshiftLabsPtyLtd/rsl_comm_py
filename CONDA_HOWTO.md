# Managing Conda environment for the project

In order to get all the dependencies in place 
for the python packages we use the `conda` environment
in this project.


[Miniconda](https://conda.io/miniconda.html) 
is a cross-platform package manager that allows managing
dependencies and creates a corresponding python *environment*. 

1) Install [miniconda](https://conda.io/miniconda.html)

2) Create the `rsl-env` environment:

`
conda env create -f environment.yml
`

Alternatively, when creating a new environment without YAML file, use:

`
conda env create -n my_environment_name
`

3) Update the `rsl-env` environment:

`
conda-env update -n rsl-env -f environment.yml
`

4) Activate the `rsl-env` environment:
Mac and Linux:
`
source activate rsl-env
`

5) Remove the `rsl-env` environment 
(delete the corresponding python packages):
`
conda env remove --name rsl-env
`