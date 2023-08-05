# The Transfer Learning in Dialogue Benchmarking Toolkit

## Overview
---
TLiDB is a tool used to benchmark methods of transfer learning in conversational AI.
TLiDB can easily handle domain adaptation, task transfer, multitasking, continual learning, and other transfer learning settings.

The main features of TLiDB are:

1. Dataset class to easily load a dataset for use across models
2. Unified metrics to standardize evaluation across datasets
3. Extensible Model and Algorithm classes to support fast prototyping




### Folder descriptions:

- /TLiDB is the main folder holding the benchmark
    - /TLiDB/data_loaders contains code for data_loaders
    - /TLiDB/data is the destination folder for downloaded datasets
    - /TLiDB/datasets contains code for datasets
    - /TLiDB/metrics contains code for loss and evaluation metrics
    - /TLiDB/utils contains utility files (data downloader, logging, argparser, etc.)
- /examples contains sample code for training models
    - /examples/algorithms contains code which trains and evaluates a model
    - /examples/models contains code to define a model
- /distances contains code for calculating distances between datasets/domains/tasks
- /dataset_preprocessing is for reproducability purposes, not required for end users. It contains scripts used to preprocess the TLiDB datasets from their original form into the TLiDB form