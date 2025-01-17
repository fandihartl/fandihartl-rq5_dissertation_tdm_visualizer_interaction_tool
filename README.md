# TDebituM Tool for Interview Data Processing, Interaction and Visualization (rq5_tdm_tool)

This repository contains tools and scripts for processing, analyzing, and visualizing interview data. It integrates with Neo4j and provides an interactive web interface using Dash.

## Features
- import and process data from multiple sources.
- visualize relationships and trends in the data.
- interactive web dashboard.

## Installation
1. clone the repository
2. navigate to the project directory
3. install dependencies 

### Packages configuration

1. Python3.8.x or higher required
2. check if pipenv is installed in your computer

    ```pipenv --version```

3. if it is not installed run `pip install pipenv` or `pip3 install pipenv`
4. in the terminal working directory run `pipenv install`
5. select the Python3.8 interpreter
6. change the file `.vscode/settings.json` the field **"python.pythonPath":** with the source of your python.exe
7. make sure the following packages are installed
   
   ```pip install pandas```

   ```pip install dash```

   ```pip install dash-bootstrap-components```

   ```pip install dash-auth```
   
   ```pip install dash-cytoscape```


Check this [Youtube Tutorial](https://www.youtube.com/watch?v=5HUL5lWkEyg) for more information. 
For more information about using virtualenv in VS Code check this [page](https://code.visualstudio.com/docs/python/environments). This project uses anaconda https://www.anaconda.com/download. 

## Usage

### Data import
To import the coded interview data to the Neo4J Aura database: 
1. use the Excel-file of the example coded interviews in ```.\TDebituM-master\Backend```
2. define the correct file path in ```.\TDebituM-master\Backend\data_import.py```
3. create an instance in [Neo4J Aura database](https://neo4j.com/product/auradb) and update the credentials in ```.\TDebituM-master\Backend\data_import.py``` at ```config.DATABASE_URL```
5. run ```.\TDebituM-master\Backend\data_import.py```
6. agree with "y" to overwrite the aura database
7. you can explore the imported TD data in [Neo4J Aura - explore](https://console-preview.neo4j.io/tools/explore)


### Data visualization
To run the plotly dash visualization locally
1. check the credentials on ```.\TDebituM-master\configuration.py```
2. run ```.\TDebituM-master\index.py``` to establish connection to database
3. run ```.\TDebituM-master\launch.py``` to start application
4. if the backend (Neo4j Aura) database is connected, Dash is running on [http://127.0.0.1:8050/](http://127.0.0.1:8050/);
5. for authentication USER: ```abcde``` and PASSWORD: ```1234```
6. use ```Ctrl+C``` to end the application

### Deployment via Heroku
To deploy the application, the current project uses the Heroku platform
1. install ```Heroku CLI``` via [Heroku CLI](https://devcenter.heroku.com/)
2. install ```git``` locally via [Git Downloads](https://git-scm.com/downloads)
3. install the software gunicorn with ```pip install gunicorn```
4. login to heroku via the git cmd with ```heroku login```

## License
This project is licensed under the MIT License. See LICENSE for details.

## Acknowledgements:
- Contributors: Fandi Hartl, Edgar Benet, and Ziyi Huang to the development and implementation of the project
- Technical advice during design and implementation: Two senior programmers in a German mid-sized software company 
- Evaluation: industrial and academic helped to refine and validate the tool
- Funding: The German Research Foundation (DFG)

## Citation
Please use the following bibtex entry:
@inproceedings{Bi2023icps
  author    = {Bi, Fandi and Vogel-Heuser, Birgit and Sapera, Edgar Benet},
  title     = {Towards an Interdisciplinary Technical Debt Interaction and Visualization Tool},
  pages     = {1--8},
  publisher = {IEEE},
  booktitle = {IEEE International Conference on Industrial Cyber-Physical Systems (ICPS)},
  year      = {2023},
  doi       = {10.1109/ICPS58381.2023.10128069}
}
