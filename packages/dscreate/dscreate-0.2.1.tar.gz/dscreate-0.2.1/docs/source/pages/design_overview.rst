
Design Overview
===============

--------
Purpose
--------

This documentation is meant for those interested in contributing to dscreate
or who are simply curious about how the software works.

**This document will cover:**

* The motivation for dscreate
* The individual components of a dscreate pipeline

----------
Motivation
----------

The origins of dscreate are based on code written by Alex Griffith in 2019, 
which...

* Splits a jupyter notebook into student facing and teacher facing content.
* Saves the student facing materials to a jupyter notebook on the ``master`` branch 
  of a git repository.
* Saves the teacher facing materials to a jupyter notebook on the ``solution`` branch 
  of a git repository.
* Saves the curriculum edit jupyter notebook to the ``curriculum`` branch
  of a git repository.

The code written in 2019 works quite well and is used to this day for generating and deploying 
Flatiron Data Science curriculum.

In 2020 Flatiron School began developing data science curriculum that used ``nbgrader``
for autograded assessments. With the introduction of nbgrader came a new splitting
procedure that needed to be applied to curriculum notebooks.

An early version of dscreate was a package that primarily included individual
scripts for these two splitting procedures. In September 2021, dscreate was rewritten 
to use an nbconvert pipeline so...

* The splitting procedures could be configured by the user.
* Users could understand the sequence of transformations without needing to read an entire ``.py`` 
  script and to prevent users from needing to understand how the "engine" works in order to understand the steps of a notebook split. 
* To ensure further development could follow consistent design conventions. 

The overall goal for this package is to centralize tooling used by the Flatiron School Data Science program, 
and to create tooling that is easily customizable and configurable so future development does not need to begin from scratch. 

The contents of ``dscreate`` include code for splitting and transforming notebooks, synchronizing branches for 
assignments pushed to github, generating tests for notebook assignments, and a command line tool for launching
a github hosted jupyter notebook in a cloud environment. 

At present, the branch splitting procedures are the most built out functionality of the package. 
The testing functionality is currently the least built out, and is an active area of development
at Flatiron School.

--------------------------------
Pipeline Components
--------------------------------

DsPipeline
----------

A DsPipeline is the top level pipeline of a notebook split procedure. They are the main functionality of notebook splitting apps
which are found in the ``apps/`` directory on github. A breakdown of the different components of a DsPipeline is visualized below. 

*Click the image to enlarge!*

.. image:: ../images/dspipeline.png
   :width: 600

A DsPipeline consists of three components.

1. A python object that reads in the curriculum jupyter notebook and
adds the notebook data to a traitlets config object. This config
Object is then passed to each step of the pipeline

2. DsConverter obkects apply transformations to the curriculum
notebook and saves the transformations to disk

3. DsController objects manage version control. Controllers exist
for git committing, pushing, merging, branch checkouts, etc.


DsConverter
-----------

A DsConverter is a nested pipeline which applies transformations to a jupyter notebook and saves the 
transformed notebook to disk. DsConverter objects rely heavily on ``nbconvert`` which does most of the heavy
lifting.

*Click the image to enlarge!*

.. image:: ../images/dsconverter.png
   :width: 600


``dscreate`` uses an ``nbconvert`` pipeline for reading in
a jupyter notebook and applying transformations to it.
Each transformation to a notebook is applied
via nbconvert preprocessors. Preprocessors apply cell
specific transformations like running cells, clearing outputs,
removing solution cells, removing hidden tests, and more.
The preprocessors are applied to the notebook by an
nbconvert exporter object which then outputs the
transformed notebook in a desired format such as
Markdown, HTML, or an updated Jupyter Notebook.
The exported notebook is then passed to an nbconvert
FilesWriter which handles saving the notebook to the
specified filetype and, when converting to markdown, saving images to a subfolder.
