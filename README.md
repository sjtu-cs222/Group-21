# Group-21
Ranking the importance of node in a complex network
## Requirements
* g++>=4.8
* python==2.7
* chainer>=5.1.0
* numpy>=1.15.4
* matplotlib>=2.2.3	
## Basic Idea
We tried to optimize the PageRank algorithm using learning to rank.
## Quick Start
We use LETOR4.0 dataset to calculate PageRank values, you can download the Gov2Link.rar from [here](https://1drv.ms/f/s!Aqi9ONgj3OqPaynoZZSZVfHPJd0).

To get PageRank values from 25,000,000 nodes, please make sure that IvtLinks. txt and PageRank.cpp are in the same directory.
 > g++ ./code/PageRank/PageRank.cpp
 > ./a.out
 To get dataset without PageRank value
 > python ./code/RankInNet/bin/build/remove_pr_value.py
  To get dataset with PageRank value
 > python ./code/RankInNet/bin/build/add_pr_value.py
 Train without PageRank value
 > python ./code/RankInNet/bin/train_without_pr.py
  Train with PageRank value
   > python ./code/RankInNet/bin/train.py
