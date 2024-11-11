# Python project for replication administration for MySQL replication.
# Classification (U)

# Description:
  Used for replication administration in a MySQL replication setup to include checking binary log status, slave status, master status, time lag between master and slave, errors detected within replication, binary log positions, and replication configuration status.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
    - FIPS Environment
  * Installation
  * Configuration
  * Program Help Function
  * Testing
    - Unit


# Features:
  * Check the slave(s) IO and SQL threads.
  * Compare master binlog position to the slaves.
  * Display the master and/or slave binlog filename and position.
  * Check time lag for the slave(s).
  * Check for errors on the slave(s).
  * Display server information for master and/or slave(s).

# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - Centos 7 (Running Python 2.7):
      -> python-pip
      -> python-devel
    - Redhat 8 (Running Python 3.6):
      -> python3-pip
      -> python3-devel

  * FIPS Environment:  If operating in a FIPS 104-2 environment, this package will require at least a minimum of pymongo==3.8.0 or better.  It will also require a manual change to the auth.py module in the pymongo package.  See below for changes to auth.py.
    - Locate the auth.py file python installed packages on the system in the pymongo package directory.
    - Edit the file and locate the \_password_digest function.
    - In the \_password_digest function there is an line that should match: "md5hash = hashlib.md5()".  Change it to "md5hash = hashlib.md5(usedforsecurity=False)".
    - Lastly, it will require the configuration file entry auth_mech to be set to: SCRAM-SHA-1 or SCRAM-SHA-256.


# Installation:

Install this project using git.
  * From here on out, any reference to **{Python_Project}** or **PYTHON_PROJECT** replace with the baseline path of the python program.

```
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-rep-admin.git
cd mysql-rep-admin
```

Install/upgrade system modules.

Centos 7 (Running Python 2.7):
```
sudo pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
NOTE: Install as the user that will run the program.

```
python -m pip install --user -r requirements3.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```


Install supporting classes and libraries.

Centos 7 (Running Python 2.7):
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mongo-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mysql-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mongo-lib.txt --target mongo_lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mongo-python-lib.txt --target mongo_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Create MySQL configuration file and make the appropriate change to the environment.
  * Change these entries in the MySQL setup:
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOST_IP"
    - name = "HOST_NAME"
    - sid = SERVER_ID
    - extra_def_file = "**PYTHON_PROJECT**/config/mysql.cfg"
    - cfg_file = "MYSQL_DIRECTORY/mysqld.cnf"

  * Change these entries only if required:
    - serv_os = "Linux"
    - port = 3306

  * If SSL connections are being used, configure one or more of these entries:
    - ssl_client_ca = None
    - ssl_client_key = None
    - ssl_client_cert = None

  * Only changes these if necessary and have knowledge in MySQL SSL configuration setup:
    - ssl_client_flag = None
    - ssl_disabled = False
    - ssl_verify_id = False
    - ssl_verify_cert = False

  * TLS version: Set what TLS versions are allowed in the connection set up.
    - tls_versions = []

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg.py
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file and make the appropriate change to the environment.
  * Change these entries in the MySQL definition file:
  * Note:  socket use is only required to be set in certain conditions when connecting using localhost.
    - password="PASSWORD"
    - socket=DIRECTORY_PATH/mysqld.sock

```
cp mysql.cfg.TEMPLATE mysql.cfg
vim mysql.cfg
chmod 600 mysql.cfg
```

Create Slave definition file and make the appropriate change for a slave connection.
  * Change these entries in the MySQL slave setup:
    - user = USER
    - japd = PSWORD
    - host = HOST_IP
    - name = HOSTNAME
    - sid = SERVER_ID
    - extra_def_file = **PYTHON_PROJECT**/config/mysql.cfg

  * Change these entries only if required:
    - cfg_file = None
    - serv_os = Linux
    - port = 3306

  * If SSL connections are being used, configure one or more of these entries:
    - ssl_client_ca = None
    - ssl_client_key = None
    - ssl_client_cert = None

  * Only changes these if necessary and have knowledge in MySQL SSL configuration setup:
    - ssl_client_flag = None
    - ssl_disabled = False
    - ssl_verify_id = False
    - ssl_verify_cert = False

  * NOTE:  Create a new set of entries for each slave in the MySQL replica set.

```
cp slave.txt.TEMPLATE slave.txt
vim slave.txt
chmod 600 slave.txt
```

Create Mongodb configuration file and make the appropriate change to the environment.
  * If submitting output to Mongo database, then require a Mongodb configuration file.
  * Make the appropriate changes to connect to a Mongo database.
    - user = "USER"
    - japd = "PSWORD"
    - host = "HOST_IP"
    - name = "HOSTNAME"

  * Change these entries only if required:
    - port = 27017
    - conf_file = None
    - auth = True
    - auth_db = "admin"
    - auth_mech = "SCRAM-SHA-1"
    - use_arg = True
    - use_uri = False

  * If connecting to a Mongo replica set:
    - repset = "REPLICA_SET_NAME"
    - repset_hosts = "HOST_1:PORT, HOST_2:PORT, ..."
    - db_auth = "AUTHENTICATION_DATABASE"

  * Notes for auth_mech configuration entry:
    - NOTE 1:  SCRAM-SHA-256 only works for Mongodb 4.0 and better.
    - NOTE 2:  FIPS 140-2 environment requires SCRAM-SHA-1 or SCRAM-SHA-256.
    - NOTE 3:  MONGODB-CR is not supported in Mongodb 4.0 and better.

  * If Mongo is set to use TLS or SSL connections, then one or more of the following entries will need to be completed to connect using TLS or SSL protocols.  Note:  Read the configuration file to determine which entries will need to be 
set.
    - SSL:
        -> auth_type = None
        -> ssl_client_ca = None
        -> ssl_client_key = None
        -> ssl_client_cert = None
        -> ssl_client_phrase = None
    - TLS:
        -> auth_type = None
        -> tls_ca_certs = None
        -> tls_certkey = None
        -> tls_certkey_phrase = None

  * FIPS Environment for Mongo:  If operating in a FIPS 104-2 environment, this package will require at least a minimum of pymongo==3.8.0 or better.  It will also require a manual change to the auth.py module in the pymongo package.  See below for changes to auth.py.
    - Locate the auth.py file python installed packages on the system in the pymongo package directory.
    - Edit the file and locate the "_password_digest" function.
    - In the "\_password_digest" function there is an line that should match: "md5hash = hashlib.md5()".  Change it to "md5hash = hashlib.md5(usedforsecurity=False)".
    - Lastly, it will require the Mongo configuration file entry auth_mech to be set to: SCRAM-SHA-1 or SCRAM-SHA-256.

```
cp mongo.py.TEMPLATE mongo.py
vim mongo.py
chmod 600 mongo.py
```

### Database Configuration

For some options to work correctly the report-host and report-port options must be added to each of the slaves mysqld.cnf file and the database restarted.
It is recommended to add these entries to all slaves including the master database.

Add the following lines to the mysqld.cnf file under the [mysqld] section.
  * report-host and report-port must match up with "name" and "port" entries respectively from the mysql_cfg.py/slave.txt file.

report-host = HOSTNAME
report-port = PORT

Restart each of the database instances for the changes to take effect.


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
{Python_Project}/mysql-rep-admin/mysql_rep_admin.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
cd {Python_Project}/mysql-rep-admin
test/unit/mysql_rep_admin/unit_test_run3.sh
```

### Code coverage:
```
cd {Python_Project}/mysql-rep-admin
test/unit/mysql_rep_admin/code_coverage.sh
```

