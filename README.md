# midas-softwarex

Contents
========
This repository contains the code use for the examples in the *MIDAS: Open-source Framework for Distributed Online
Analysis of Data Streams* paper. The structure of the repository is as follows

```
root
├── data
├── python
│   ├── example_1
│   │   
│   ├── example_2
│   │   
│   └── example_3
└── R

```
- Data-directory contains all the input data used in the examples as csv-files
- Python-directory contains the code and configuration files
- R-directory contains analysis scripts for offline analysis of the input signals

Instructions
============
Examples can be run from a terminal in the corresponding example directory. Below is step-by-step instruction how to run example 1. Other examples follow the same structure but the number of streams and nodes varies.

- Run the streamer script (if one is provided) which reads input data and streams it over LSL
```
$ python stream_mental_workload_data.py
```
- Start the node(s) from the command line. Use the provided configuration file and corresponding configuration section
```
$ python ecg_node.py config.ini ecg
$ python eeg_node.py config.ini eeg
```
- Start dispatcher with the provided configuration file
```
$ midas-dispatcher config.ini dispatcher
```
- Start the client script
```
$ python3 mental_workload_client.py
```
