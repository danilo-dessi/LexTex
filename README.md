# LexTex
This repository contains the LexTex sources, the main outcome of the work: LexTex: A Novel FrameWork to Automatically Assign Scores to Word Senses in Domain Specific Categories

LexTex is a python developed tool that enables to build new lexicons starting from a set of annotated resources. It is written in python end exploits functionalities of Stanford Core NLP and UKB.

Authors: Danilo Dessi' and Diego Reforgiato Recupero


# Contents
<strong> src/ </strong> contains source codes for building a new WordNet synsets-based lexicon. It also includes a script for labeling new resources with the generated lexicon. 

<strong> training_data/ </strong> contains training data that is employed to build our lexicons.

<strong> test/ </strong> contains test data and scripts used for the evaluation.

<strong> lexicons/ </strong> contains all lexicons built and evaluated in this work.

<strong> results-supervised/ </strong> contains the scores predicted with the supervised methods Decision Trees, Random Forests, and Support Vector Machine


Data used for the comparison with supervised methods are available in:

Employee: https://www.kaggle.com/petersunga/google-amazon-facebook-employee-reviews

TripAdvisor: http://nemis.isti.cnr.it/~marcheggiani/datasets/

Laptops: https://github.com/davidsbatista/Aspect-Based-Sentiment-Analysis/tree/master/datasets/ABSA-SemEval2015


# Installation

## Requirements
Python version >= 3.6

Java version >= 1.8

Install other requirements with: pip3 install -r src/requirements.txt

Finally, download the stopwords module of nltk with python3 -m nltk.downloader stopwords

## Other software
LexTex uses corenlp-server and ukb-3.1 in its pipeline. Please use this versions.

* <strong> ukb-3.1/ </strong> can be downloaded from http://ixa2.si.ehu.es/ukb/. Extract the archive under the LexTex directory. Compile its KB following the point 1.2 of its README (see readme under the ./script directory). In our experiments we employed the version 3.0 of WordNet.

* <strong> stanford-corenlp-full-2018-10-05 </strong> can be downloaded from https://stanfordnlp.github.io/CoreNLP/. Extract the archive under the LexTex directory. 


## How to use
To use LexTex the command python3 LexText.py <parameters> must be executed. 
Accepted parameters are:

* -d, --directory <value>: the direcry that contains all resources that will be employed to generate a new lexicon (<strong>mandatory</strong>)

* -m, --mode <value>: the mode with which UKB will be used by the Word Sense Disambiguation Module. The default mode is *ppr_w2w*.

* -c, --categories <value>: the number of categories (<strong>mandatory</strong>)
  
* -lc, --label-categories <value>: the list of categories separated by coma (es. joy,sadness,fear)
 
* -ln, --lexicon-name <value>: the name that will be assiged to the lexicon 

* -nn, --no-norm: flag that indicates that averages over categories must not be normalized

* -nc, --no-coeff: flag that indicates that averages over categories must not be weighted with "cf"

<strong> Examples </strong>

python3 LexTex.py -d training -c 5 

python3 LexTex.py -d training -c 5 -ln my_new_super_lexicon

python3 LexTex.py -d training -c 5 -m ppr_w2w -ln my_new_super_lexicon++

python3 LexTex.py -d training -c 5 -m ppr_w2w -ln my_new_super_lexicon++ --no-coeff


# Input
Input files must be added into a unique directory. Each row of a file must contain a text followed by a score for each categories. The separation character must be '\t'.


# Output
The output is a lexicon where in each row there is a WordNet synset and a value for each input category. See the directory lexicons for examples.
  
Planned developments and fixes:
  - adding the headers to columns of generated lexicons

