million-dollar-homepage-checker
===============================

How many of the advertised websites on The Million Dollar Homepage are still up?

[TODO: generate report of results and create an updated bitmap that blacks out the dead sites.]

##### USAGE

First, get all the required Python packages:

    $ pip install -r requirements.txt

(If you don't have `pip`, you will need to [install](http://http://www.pip-installer.org/en/latest/installing.html) it first.)

Now check your OS's limit on open files. This script issues over 3300 `GET` or `HEAD` calls in a batch. Such a volume of TCP connections required may exceed your system limit. For example, to check the limit:

    $ ulimit -n
    256

In this case, 256 is too low. Let's bump it up to 4096 for this session:

    $ ulimit -n 4096

Now run the script:

    $ python src/check.py
