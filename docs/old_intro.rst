

============
Introduction
============

.. figure:: images/question_capture.png
	:align: left
	:alt: Sample run of Quails
	
	Sample run of Quails


Quails is a modular question answering framework that is meant to provide a testbed for the author's dissertation work.  It has been designed to be fully customizable at every step of a user specified question answering pipeline.

A high level example of a question answering pipeline, represented as a list, is as follows:

1.  Receive a natural language question from a user.
2.  Extract natural language features from the question.
3.  Determine the type of answer required by the question using one or more classification algorithms.
4.  Construct a logical representation of the question using information gathered in the previous steps.
5.  Use the logical representation to build a query to search for documents that may contain information relevant to the question.
6.  Search the documents for possible answers.
7.  Rate the answers based on how likely they are to answer the question.
8.  Return the answers and their scores to the user. 

The system is comprised of two primary parts. The first component is a Flask server providing question answering pipeline services such as NLP, classification, text indexing, answer extraction, and answer scoring.  

The second component is an interface program which receives a natural language question from the user and acts as a controller for the question answering pipeline in order to produce an answer.


