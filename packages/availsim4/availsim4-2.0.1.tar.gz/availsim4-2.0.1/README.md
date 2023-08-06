# AvailSim4

Availsim 4 is a software to predict reliability and availability of modern particle accelerators and the related
technical systems. It is based on a Monte Carlo Discrete Event Simulation algorithm and allows for advanced availability
and reliability statistics.

## Requirements

Python >=3.7, <4

## Installation

### Pre-requirement for Windows users

- One of the external dependencies requires Windows users to install Microsoft Visual C++ 14.0 or greater. It can be downloaded from "Microsoft C++ Build Tools": <https://visualstudio.microsoft.com/visual-cpp-build-tools/>, this requirement is needed to use the Quasi-Monte-Carlo algorithm. CERN's Window users might prefer to use SWAN notebooks which are running on Linux machines.

### (Optional) Visualization tools

- To generate a diagram of the architecture tree, AvailSim4 requires PyGraphviz package and Graphviz to be installed. More information and OS-specific installation guide of Graphviz: <https://graphviz.org/download/> and of PyGraphviz: <https://pygraphviz.github.io/documentation/stable/install.html>. General instructions: 
  - **Linux**: install Graphviz through your system package manager and then make sure to install PyGraphviz with `pip` or `conda` : `apt-get update`, `apt-get install libgraphviz-dev`, `pip install pygraphviz`.
  - **Windows**: Graphviz installation wizard can be downloaded manually from the website. Then proceed to install PyGraphviz with `pip` or `conda`. Make sure that `dot` program's plugins are configured by running `dot -c` command in your environment. May also require Microsoft C++ Build Tools as a pre-requirement .   
  - **MacOS**: you can install Graphviz using Homebrew package manager by running command `brew install graphviz` and then `pip install pygraphviz`.

### Gitlab

- Clone the project from <https://gitlab.cern.ch/availsim4/availsim4core>
- (Optional) create a dedicated virtual environment. In the context of CERN
  follow : <https://wikis.cern.ch/display/ACCPY/Getting+started+with+Acc-Py>
- Install the dependencies ```pip install -r requirements.txt``` or ```conda install --file requirements.txt```
- For CERN users, dependencies could be installed in a dedicated folder to ease the load on the file system when executing larger number of jobs in parallel:
```pip install --target=/afs/cern.ch/work/U/USERNAME/pipinstall -r requirements.txt``` (see user guide, `Running the code` section)

### pypi

- From CERN network you can use the internal Python Package Index (<https://acc-py-repo.cern.ch>)
  ```pip install availsim4```

## Usage

AvailSim4 input arguments are the following ones:

```bash
availsim4.py [-h] 
             --system SYSTEM
             --simulation SIMULATION 
             --output_folder OUTPUT_FOLDER
             [--sensitivity_analysis SENSITIVITYANALYSIS] 
             [--HTCondor]
             [--HTCondor_extra_argument OPTIONAL_EXTRA_ARGUMENT]
             [--nb_processes NB_PROCESS]
             [--children_logic PYTHON_FILE]
```

Example of a call for an execution on a local machine within a terminal:

```bash
python3 availsim4.py --system availsim4core/test/E2E/input/convergence/convergence_test_system.xlsx --simulation availsim4core/test/E2E/input/convergence/N1000_simulation.xlsx --output_folder output/E2E_example/
```

A notebook, `call_AvailSim4.ipynb`, is provided to make calls to AvailSim4 in jupyter (e.g. SWAN for CERN users).

Example of a call for an execution on a cluster handle with HTCondor is described in the user guide.

## User documentation

A guide is provided in `doc/user_guide/`

## License
Copyright © CERN 2021. Released under the [GPL 3.0 only license](LICENSE). All rights not expressly granted are reserved.
