# Open Data for Experimental Mechanics: the platform

The purpose of the project is to develop and maintain a platform aimed at sharing experimental data and results for the field of experimental mechanics.
The availability of experimental results is limited, because they are scattered in publications.
The access to experimental data could be beneficial for mechanical engineers and computational engineers to improve their research.
Inside a publication, details necessary to reproduce the experiment or design the simulation for a benchmark are often missing.
Therefore, it appears that a platform could be used to share experimental data sets in mechanics,
rating them with respect to reproducibility and quality of the experimental setup. Such data sets could be used for benchmarks with simulation results, to check if some experiments have already been done and maybe slightly change the initial plan.
Thus, both communities could enhance the understanding of material behavior and fasten their research.

If you would like to learn even more about the project and how it came to be, please [take a look at the first post on our blog here](https://opendataexpmechanics.github.io/ODEM-project/).

You should be able to test the current version of the platform here.

## Want to contribute ?

If you would like to contribute and help improve the project, please take a look at our [Contributing to Open Data for Experimental Mechanics guide](https://github.com/OpenDataExpMechanics/platform/blob/master/CONTRIBUTING.md).

## Testing the platform on your local machine (dev purposes)

This guide was written for Ubuntu. You can easily install Ubuntu on a virtual machine using one of the many guides available online. It should be possible to do these steps on any other OS. The guide does not specify anything (yet) about using a virtual environment, but we recommend that you do so.

### Getting the code

Copy the `ssh` address of this repository (provided in the top right corner of this page) in your clipboard. Open a terminal (using `Ctrl`+`Alt`+`T`) and paste the following line:

`sudo apt-get install git`

Then:

`git clone git@github.com:OpenDataExpMechanics/platform.git`

You should now have a folder called `platform`:

```terminal
ilyass@DESKTOP-KCDKG6L:~/Repositories/ODEM$ ls
platform
```

You now have the necessary code to execute the Open Data for Experimental Mechanics code on your machine.

## Dependencies

### Packaged software

You now need to install all the other packages necessary to execute the platform code.

Paste the following line in your terminal:

`sudo apt-get install mariadb-server python-dev python-pip curl libcurl4-openssl-dev libsox-dev`


### Setting the database

`mysql -u root -p`

If you get an error saying the mysql database is not available (something like this `ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2 "No such file or directory")
`), try starting MariaDB (the database used for the platform) using `sudo /etc/init.d/mysql start`.

One your are able to successfully enter the mysql prompt space, copy-paste the content of the `database.sql` file (available in the repository) line by line to your terminal, and execute them one after the other.

Retart mysql server.

### Python packages

* pyaml
* MySQL-python
* web.py

Installing the necessary python packages is pretty straight forward. A file called `requirements.txt` is in the repository. Go to the repository folder and execute:

`sudo pip install -R requirements.txt`


### Configuration

Please provide in the main directory a yaml file with these attributes for the connection to the database.

```yaml
Database:
    User:
    Database:
    Password:
    Type: mysql
    Host:
```

## Start the platform

`python main.py`
