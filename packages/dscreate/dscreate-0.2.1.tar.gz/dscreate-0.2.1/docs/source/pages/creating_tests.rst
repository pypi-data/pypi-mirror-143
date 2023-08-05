.. _creating-tests:

Creating Tests
==============

`dscreate` offers a couple options for adding tests to your curriculum materials.

NOTE: All tests are created and run using the `Tests` class within the `compose.tests` subdirectory.::

         from dscreate.compose.tests import Tests
         tests = Tests()

Below, is an example of a test for a simple problem. In this scenario a student is
tasked with generating the list ``[1,2,3]``. 

------------------------         
Writing Test Functions
------------------------
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

::

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

::

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

::

      >>>output_test: Your function returned -1, but should return 3!
      >>>output_test: Your function returned the correct answer for 1 + 2!

---------------------       
Writing a Test Class
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

::

         >>>test_for_attribute: ✅
         >>>test_method_output: Your method correctly returned 5!

::

         class StudentSolutionWrong:
            
            def method(self):
               return 3

         tests.run('Class_Example', StudentSolutionWrong)

::

         >>>test_for_attribute: ❌
         >>>test_method_output: Your method returned 3 when it should have returned 5!
