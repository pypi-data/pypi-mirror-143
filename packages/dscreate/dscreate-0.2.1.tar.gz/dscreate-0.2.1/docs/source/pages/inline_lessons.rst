Inline Lessons
==============

**The overall proccess looks like this**

* Create project folder
* ``cd`` into the the project folder
* Open a ``curriculum.ipynb`` jupyter notebook
* Create lesson using `solution tags <#solution-cells>`_ 
* Save the curriculum notebook
* run ``ds create --inline``
* Push repository to github
* Copy link to the top level ``index.ipynb`` file on github.
* run ``ds share <github link>``
* A student link is added to your clipboard. Then you share it!

**To make new edits to a lesson after running** ``ds create --inline``

* run ``ds edit``
* Open the ``curriculum.ipynb`` notebook
* Make edits in curriculum notebook
* Save notebook
* run ``ds create --inline``


Lesson Structure
==================

This toolkit uses the following directory structure for all lessons::

   lesson-directory 
         |
         index.ipynb
         curriculum.ipynb
         data
            |
            lesson_data.csv
         .solution_files
            |
            index.ipynb
            .test_obj
               |
               pickled_test.pkl 

* The top level ``index.ipynb`` file contains all student facing materials.
* The top level ``curriculum.ipynb` file is where all curriculum materials are created.
* The `data/` folder is not required, but tends to be best practice for most data science projects.
* The ``.solution_files`` hidden folder stores the solution content.
* The ``.solution_files/index.ipynb`` file is the notebook containing all solution code and markdown.
* The ``.test_obj`` folder contains all pickled test objects. See `Creating Tests <#test-code>`_