# platform

### Development setup

`mysql -u root -p`
Forwindows bash users, start MariaDB with `sudo /etc/init.d/mysql start`
Then execute `database.sql` line by line.
Retart mysql server.

Also: `sudo apt-get install libmariadbclient-dev python-dev python-pip curl libcurl4-openssl-dev libsox-dev`
Then execute `requirements.txt`:
`pip install -R requirements.txt`

`python main.py`


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

### Dependencies
* pyaml
* MySQL-python
* web.py
