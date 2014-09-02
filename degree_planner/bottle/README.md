Visualization for Alveo 
========================
The project aims at developing some graph visualization communicating with the dataset available at **The Alveo Project (hcsvlab.org.au).**
It uses ``Bottle``, a python framework for the web server and Bootstrap for the frontend.

### Requirements
1. [pyhcsvlab library](https://github.com/Alveo/pyhcsvlab)
2. [Alveo Account with API Key](http://hcsvlab.org.au)

### Usage

1. Download the ``configuration file`` from [Alveo Account](http://hcsvlab.org.au) and put it under home directory (~)
2. If you have not installed [hcsvlab library ](https://github.com/Alveo/pyhcsvlab), download the library and provide the ``path to that library in main.py file``
3. In the terminal at this directory, run the command ``python main.py``
4. Open your browser and navigate to ``localhost`` with the port specified in the terminal screen


### Screenshots
#### WordCloud
![](/static/images/wordcloud.png)


#### Heatmap
![](/static/images/heatmap.png)


#### Frequency Timeline
![](/static/images/frequency_timeline.png)

The graph visualizations are based on ``D3.js`` [https://github.com/mbostock/d3/wiki/Gallery](https://github.com/mbostock/d3/wiki/Gallery)