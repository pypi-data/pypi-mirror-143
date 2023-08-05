CLI Tools
===========

-------------
Master, Curriculum, Solution
-------------

``ds create``

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
``nbgrader`` Master, Solution
-------------

``ds generate``

**Requirements:**

- This command must be run from a `master` branch
- An `index.ipynb` file must exist on the `master` branch

**When this command is run the following things happen:**

- The assignment is generated via the NbGrader API
- The source notebook is convered to markdown and saved as a README on the `master` branch
- The `master` branch is merged into the `solution` branch
- The release notebook is converted to markdown and saved as a README on the `master` branch
- Changes are pushed to github for each branch


-------------
In directory split
-------------

``ds create --inline``

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
Once edits are complete, run ``ds create`` to hide the solutions inside a hidden folder.

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


