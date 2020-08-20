# COVID-19 Risk Estimation
This repository contains the work conducted by Sedevizo Kielienyu for community risk estimation of COVID-19 under the supervision of Dr. Burak Kantarci. Documentation for the Python codes are generated using Sphinx and can be found under the 'Documentation' folder. Details regarding the input files and output files of the code are given below, along with the pre-requisites that is required for this project:

1. **Pre-requisites**:
  Programming Language: The baseline programming language is Python, which is used to create all the functions regarding the risk modelling. For plotting the graphs, MATLAB is       used. Python version for this project is 3.8.4 and MATLAB version is R2020a. 
  
    Python libraries: Here, the libraries(modules) used for this project are listed.  
    &nbsp;&nbsp;a. pandas  
    &nbsp;&nbsp;b. numpy  
    &nbsp;&nbsp;c. hmmlearn  
    &nbsp;&nbsp;d. sklearm    
    &nbsp;&nbsp;e. time  
  
2. **Input file (Raw data)**:
  The raw data (mobility pattern) is generated using Crowdsensim<sup>1</sup>. Crowdsensim is a simulator used to create realistic crowdsensing and crowd-management simulation in     an urban setting of a real city map.</br> 
  The raw data (mobility pattern) has 7 features defined by the tuple <UserID, Latitude, Longitude, Altitude, Day, Hour, Min>. The simulation was performed in two scenario of       10,000 users and 30,000 users, respectively, where Day = 1. The raw data can be found in 'Raw Data' folder. 'Raw Data' folder contains two sub-folders, each representing one       the two scenarios. The folders are labelled as 'City-Users-Day'. Here is a snippet of the raw data.
  <img src="images/raw_data.png" width=800>

3. **Output files**:
  The raw data is cleaned using Microsoft Excel. 
  

