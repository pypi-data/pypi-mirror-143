.. dscreate documentation master file, created by
   sphinx-quickstart on Wed Apr 28 17:16:41 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================================
`dscreate`
====================================

*Flatiron School Data Science Toolkit*

`Read the docs <https://dscreate.readthedocs.io/>`_


Installation
============
* run ``pip install dscreate``


CLI Tools
==================

**Arguments that apply for all notebook split applications:**

``--local``
   - This argument disables the ``PushController``. Changes are committed but are not pushed.

``--execute=<bool>``
   - By default, the solution code cells are run when a notebook is split. ``--execute=False`` disables the ``ExecuteCells`` preprocessor. 

``-m``
   - This argument functions like the ``-m`` git argument, and allows you specify the commit message.


-------------
``ds create``
-------------
**Requirements:**

- This command must be run from a `curriculum` branch
- An `index.ipynb` file must exist on the `curriculum` branch

**When this command is run the following things happen:**

- A README.md file if generated for the curriculum notebook
- The curriculum notebook is split
   - Student facing materials are added to an `index.ipynb` file on the `master` branch
   - Solutions are added to to an `index.ipynb` file on the `solution` branch
- READMEs and created for both `master` and `solution` branches
- Changes are pushed to github for each branch


-------------
``ds generate``
-------------

**Requirements:**

- This command must be run from a `master` branch
- An `index.ipynb` file must exist on the `master` branch

**When this command is run the following things happen:**

- The source notebook is converted to markdown and saved as a README on the `master` branch
- The `master` branch is merged into the `solution` branch
- The release notebook is converted to markdown and saved as a README on the `master` branch
- Changes are pushed to github for each branch

-------------
``ds create --inline``
-------------
**Requirements**

- A `curriculum.ipynb` notebook must exist.

**When this command is run the following things happen:**

- An ``index.ipynb`` file is added to the current working directory containing all "student facing" content within the ``curriculum.ipynb`` file
- An ``index.ipynb`` file is added to the ``.solution_files`` subdirectory containing all solution content in the ``curriculum.ipynb`` file.
- The ``curriculum.ipynb`` file is deleted
  
   - To make future edits to this project, the curriculum notebook must be generated using `ds edit`.

-------------
``ds edit``
-------------
When this command is run the following things happen:

* The metadata inside the lesson and solution notebooks is used to recompile the ``curriculum.ipynb`` notebook.

Once the curriculum notebook is compiled, edits to the lesson can be made inside ``curriculum.ipynb``.
Once edits are complete, run ``ds create --inline`` to hide the solutions inside a hidden folder.


-------------
``ds share <Github notebook url>``
-------------

* This command accepts any link that points to a public notebook on github. When this command is run, a link is copied to your clipboard that points to the notebook on illumidesk.
* This command can be used to create `url module items in canvas <https://community.canvaslms.com/t5/Instructor-Guide/How-do-I-add-an-external-URL-as-a-module-item/ta-p/967>`_.

-------------
``ds config``
-------------
When this command is run, a path pointing to a dscreate configuration file is printed.

**Printing the global configuration file**

``ds config``

**Printing the configuration file for a specific application**

``ds config create``

or 

``ds config generate``

-------------
``ds markdown <path to jupyter notebook>``
-------------
When this command is run, a jupyter notebook is converted to markdown.

This command defaults to naming the resulting markdown file as ``README.md``, but 
this can be customized by passing in ``--output=<name of notebook>``

**Example:**

``ds markdown index.ipynb``

This produces a ``README.md`` version of `index.ipynb``

``ds markdown index.ipynb --output=textfile.md``
This produces a ``textfile.md`` version of ``index.ipynb``.

-------------------------------------------------------

.. _creating-a-lesson:

Creating an Inline Split Lesson 
==================

**The overall proccess looks like this**

1. Create project folder
2. ``cd`` into the the project folder
3. Create a `curriculum.ipynb` notebook
4. Open the ``curriculum.ipynb`` jupyter notebook
5. Create lesson using `solution tags <#creating-solution-cells>`_ 
6. Save the curriculum notebook
7. run ``ds create --inline``
8. Copy link to the top level ``index.ipynb`` file on github.
9. run ``ds share <github link>
10. Share link with students. 

**To make new edits to a lesson after running ``ds -create``**

1. run ``ds edit``
2. Open the ``curriculum.ipynb`` notebook
3. Make edits in curriculum notebook
4. Save notebook
5. run ``ds create --inline``

Creating Solution Cells
=======================

What ``ds create`` is used, all solution cells are removed from the edit file 
and moved to the ``index.ipynb`` file dedicated for solutions.

Solution cells can be created for both code and Markdown cells in Jupyter Notebooks.

**To create a solution Markdown cell**

Place ``==SOLUTION==`` at the top of a Markdown cell. This tag should have its own line.

**To create a solution code cell**

Place ``#__SOLUTION__`` or ``#==SOLUTION==`` at the top of the code cell. This tag should have its own line.

.. _test-code:

Creating Tests
==============

`dscreate` offers a couple options for adding tests to your curriculum materials.

NOTE: All tests are created and run using the `Tests` class within the `compose.tests` subdirectory.::

         from dscreate.compose.tests import Tests
         tests = Tests()

------------------------         
Writing Test Functions
------------------------

Below, is an example of a test for a simple problem. In this scenario a student is
tasked with generating the list ``[1,2,3]``. 

::

         #__SOLUTION__

         def test_function(student_answer):
            if student_answer == [1,2,3]:
               return True


         tests.save(test_function, 'first_test')

**Running a test**::

         student_solution = [1,2,2]

         tests.run('first_test', student_solution)
         tests.run('first_test', [1,2,3])

         >>>first_test: ❌
         >>>first_test: ✅

**Test function can use multiple arguments**::

         #__SOLUTION__
         def multiple_arg_test(arg1, arg2, arg3, arg4):
            if arg1 != [1,2,3]:
               return False
            elif arg2 != [3,2,1]:
               return False
            elif arg3 != 'hello world':
               return False
            elif arg4 != 51:
               return False
            else:
               return True
            
         tests.save(multiple_arg_test, 'multiple_arguments')

**Running a multiple argument test**::

         student_answer = [1,2,3], [3,2,1], 'hello world', 51
         tests.run('multiple_arguments', *student_answer)

         student_answer = [1,2,3], [3,2,1], 'hello flatiron', 51
         tests.run('multiple_arguments', *student_answer)

         >>>multiple_arguments: ✅
         >>>multiple_arguments: ❌

**If you would like to output the result of the test instead of ✅ or ❌, you can set assertion=False**::

         #__SOLUTION__
         def output_test(function):
            def solution(a,b):
               return a+b
            
            student = function(1,2)
            answer = solution(1,2)
            if student != answer:
               return f"Your function returned {student}, but should return {answer}!"
            else:
               return f'Your function returned the correct answer for 1 + 2!'
            

         tests.save(output_test, 'output_test', assertion=False)
   
**Running a test that returns the output of the test function**::

      def student_answer_wrong(a,b):
         return a-b

      def student_answer_correct(a,b):
         return a+b

      tests.run('output_test', student_answer_wrong)
      tests.run('output_test', student_answer_correct)

      >>>output_test: Your function returned -1, but should return 3!
      >>>output_test: Your function returned the correct answer for 1 + 2!

---------------------       
Writing A Test Class
---------------------

If you have multiple tests you'd like to run, the easiest solution would be create a class like below

* *All test methods must begin with the word `test`*
* If you would like to return the output of a test, set the argument `output=True` for the test method.

**Below is an example of a test class for the following student task:**

   "In the cell below, create a class that has an attribute called "attribute" and a method called "method". 
   The method should return the number 5."



::

         #__SOLUTION__
         class ExampleTest:
            
            def __init__(self, student_answer):
               self.student_answer = student_answer()
               
            def test_for_attribute(self):
               if hasattr(self.student_answer, 'attribute'):
                     return True
               
            def test_method_output(self, output=True):
               try:
                     result = self.student_answer.method()
                     if result == 5:
                        return 'Your method correctly returned 5!'
                     else:
                        return f'Your method returned {result} when it should have returned 5!'
               except:
                     return 'Your method threw an error.'
                     
                     
         tests.save(ExampleTest, 'Class_Example')


**Running the test class**::

         class StudentSolutionCorrect:
            
            def __init__(self):
               self.attribute = True
               
            def method(self):
               return 5
            
         tests.run('Class_Example', StudentSolutionCorrect)

         >>>test_for_attribute: ✅
         >>>test_method_output: Your method correctly returned 5!

::

         class StudentSolutionWrong:
            
            def method(self):
               return 3

         tests.run('Class_Example', StudentSolutionWrong)

         >>>test_for_attribute: ❌
         >>>test_method_output: Your method returned 3 when it should have returned 5!
