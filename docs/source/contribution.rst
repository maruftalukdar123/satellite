How to Contribute to the repository
===================================

First time setup
----------------

-   Download and install the "latest version of git".
-   Configure git with your "username" and "email".

    .. code-block:: text

        $ git config --global user.name 'your name'
        $ git config --global user.email 'your email'

-   Make sure you have a "GitHub account".
-   "Clone" the main repository locally.

    .. code-block:: text

        $ git clone git@github.com:UCL-COMP0233-22-23/aigeanpy-Working-Group-10.git


Start coding
------------

-   Create a branch to identify the issue you would like to work on. If
    you're submitting a bug or documentation fix, branch off of the
    latest ".x" branch.

    .. code-block:: text

        $ git fetch origin
        $ git checkout -b your-branch-name origin/2.0.x

    If you're submitting a feature addition or change, branch off of the
    "main" branch.

    .. code-block:: text

        $ git fetch origin
        $ git checkout -b your-branch-name origin/main

-   Using your favorite editor, make your changes,
    "committing as you go".
-   Include tests that cover any code changes you make. Make sure the
    test fails without your patch. Run the tests as described below.
-   Push your commits to your fork on GitHub and
    "create a pull request". Link to the issue being addressed with
    ``fixes #123`` in the pull request.

    .. code-block:: text

        $ git push --set-upstream fork your-branch-name

Running the tests
-----------------

Run the basic test suite with pytest.

.. code-block:: text

    $ pytest

This runs the tests for the current environment, which is usually
sufficient. CI will run the full suite when you submit your pull
request. You can run the full test suite with tox if you don't want to
wait.

.. code-block:: text

    $ tox

Code Style
-----------------

Your code should be readable. Clear code and file structure for all the functions and classes definitions are
also required. Objects should be represented in the correct format.

