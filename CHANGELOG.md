# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [5.1.1] - 2025-05-09

### Fixed
- create_filename: Removed subject line from being the default filename for the email attachment.
- main: Added "-f" to opt_val_list to ensure a value is passed in with the argument and made "-f" a required argument if "-r" option is passed.

### Changes
- data_out: Removed passing in subject line to create_filename function.


### Changed
- Documentation changes.


## [5.1.0] - 2025-04-11
- Added ability to send data in an email as attachment.
- Updated python-lib v4.0.1
- Updated mysql-lib v5.5.0

### Added
- create_filename: Creates a filename for the attachment to an email.

### Changed
- call_run_chk: Added gen_class.TimeFormat instance and pass instance to data_out function.
- data_out: Set up check to email output as an attachment using gen_class.Mail2 class, called create_filename to get filename for attachment and replaced args.get_val with args.arg_exist.
- Documentation changes.

### Removed
- Support for MySQL 5.6/5.7


## [5.0.0] - 2025-02-04
Breaking changes

- Removed support for Python 2.7.
- Removed Mongo insert option.
- Updated mysql-lib v5.4.0
- Updated python-lib v4.0.0

### Added
- process_time_lag: Check to see if the time lag still exists
- chk_other: Print any possible problems found.

### Changed
- chk_slv_other: Replaced \_chk_other call with chk_other call.
- chk_slv_time: Replaced \_process_time_lag call with process_time_lag call.
- data_out: Removed Mongo code.
- Replaced list() with [].
- Converted strings to f-strings.
- Documentation changes.

### Deprecated
- Support for MySQL 5.6/5.7

### Removed
- \_chk_other function.
- \_process_time_lag function.


## [4.0.10] - 2024-11-18
- Updated python-lib to v3.0.8
- Updated mongo-lib to v4.3.4
- Updated mysql-lib to v5.3.9

### Fixed
- Set chardet==3.0.4 for Python 3.


## [4.0.9] - 2024-11-08
- Updated chardet==4.0.0 for Python 3
- Updated distro==1.9.0 for Python 3
- Updated protobuf==3.19.6 for Python 3
- Updated mysql-connector-python==8.0.28 for Python 3
- Updated psutil==5.9.4 for Python 3
- Updated mongo-lib to v4.3.3
- Updated mysql-lib to v5.3.8
- Updated python-lib to v3.0.7

### Deprecated
- Support for Python 2.7


## [4.0.8] - 2024-09-27
- Updated pymongo==4.1.1 for Python 3.6
- Updated mongo-lib to v4.3.2
- Updated python-lib to v3.0.5
- Updated mysql-lib to v5.3.7


## [4.0.7] - 2024-09-04
- Updated pymongo to v4.6.3 for Python 3.
- Updated mongo-libs to v4.3.1

### Changed
- chk_slv_err, chk_mst_log:  Refactored functions.
- main: Removed parsing from gen_class.ArgParser call and called arg_parse2 as part of "if" statement.


## [4.0.6] - 2024-04-23
- Updated mongo-lib to v4.3.0
- Added TLS capability for Mongo
- Set pymongo to 3.12.3 for Python 2 and Python 3.

### Changed
- Set pymongo to 3.12.3 for Python 2 and Python 3.
- config/mongo.py.TEMPLATE: Added TLS entries.
- Documentation updates.


## [4.0.5] - 2024-03-11
- Updated mysql-lib to v5.3.5

### Fixed
- chk_slv_time, chk_slv_other, chk_mst_log, chk_slv, chk_slv_err: Check to see if slave is down and update slave list.

### Changed
- rpt_slv_log:  Replaced down slaves nulls with Unknown value.
- add_miss_slaves: Replaced using Name of the slave with the slaves UUID.
- chk_slv_time:  Added slave_uuid to each slave dictionary in JSON object.
- \_process_time_lag:  Replaced check for None with check for "null".
- data_out: Replaced call to dict_out with call to gen_libs.dict_out.

### Removed
- dict_out:  Replace by gen_libs.dict_out


## [4.0.4] - 2024-02-26
- Updated to work in Red Hat 8
- Updated mysql-lib to v5.3.4
- Updated mongo-lib to v4.2.9
- Updated python-lib to v3.0.3

### Changed
- main:  Removed the gen_libs.get_inst call.
- Set simplejson to 3.12.0 for Python 3.
- Set chardet to 3.0.4 for Python 2.
- Documentation updates.


## [4.0.3] - 2023-05-25
### Fixed
- data_out: Fixed incorrectly setting the email subject line.

### Changed
- main: Updated gen_libs.help_func call to the new version.


## [4.0.2] - 2022-10-11
- Updated to work in Python 3 too
- Upgraded python-lib to v2.9.4
- Upgraded mysql-lib to v5.3.2
- Upgraded mongo-lib to v4.2.2

### Changed
- \_process_time_lag: Refactored "if" statement to check for Nonetype datatype first.
- Converted imports to use Python 2.7 or Python 3.

### Fixed
- main: Set up and passed file_perm variable to arg_file_chk method.


## [4.0.1] - 2022-06-29
- Added TLS capability
- Added ability to override postfix and use mailx command.
- Added -x option to allow the -T option to return none for email use.

### Fixed
- main: Added -x option for the -T option.
- chk_mst_log: Fixed problem of appending chk_slv function data to SlaveLogs list.

### Added
- is_time_lag: Checks to see if there is a time lag.

### Changed
- chk_slv_err, \_chk_other: Added "Status" key to IO and SQL error dictionaries.
- call_run_chk: Added check to see if -x option is set and if there is a time lag detected.
- data_out: Added option to send_mail call to override postfix and use mailx command.
- config/slave.txt.TEMPLATE: Added TLS entry.
- Documentation updates.


## [4.0.0] - 2022-06-02
Breaking change

- Changed the program to operate using JSON formats only.
- Replaced args_parser module with the gen_class.ArgParser class.
- Upgrade mysql-connector to v8.0.22.
- Upgrade mysql-libs to v5.3.1.
- Upgrade mongo-libs to v4.2.1.
- Upgrade python-lib to v2.9.2.

### Added
- data_out: Outputs the data in a variety of formats and media.
- dict_out: Print dictionary to a file, standard out, and/or an email instance either in expanded or flatten JSON format.

### Changed
- call_run_chk: Removed any data out commands as this was moved to data_out function.
- \_chk_other: Replaced string standard output with JSON format and returned only those entries with problems detected.
- \_process_time_lag: Removed standard output and returned only the time lag.
- add_miss_slaves: Changed from modifying the check slave time dictionary to returning a list of missing slaves.
- rpt_mst_log, rpt_slv_log, chk_mst_log, chk_slv_thr, chk_slv_err, chk_slv_time, chk_slv_other: Converted output to dictionary and returned results to calling function.
- main, run_program, call_run_chk: Replaced the use of arg_parser (args_array) with gen_class.ArgParser class (args).
- main, call_run_chk: Changed "-b" option to "-i" option to be inline with the other programs.
- config/mysql_cfg.py.TEMPLATE: Added TLS version entry.
- config/mongo.py.TEMPLATE: Removed old entries.
- Documentation updates.

## Removed
- \_process_json: Replaced with data_out function.


## [3.2.0] - 2021-08-19
- Updated to work in MySQL 8.0 and 5.7 environments.
- Updated to work in a SSL environment.
- Updated to use the mysql_libs v5.2.2 library.
- Updated to use gen_libs v2.8.4 library.

### Changed
- \_chk_other:  Check version to determine how to process retry and refactored the "if" statements.
- chk_slv_other:  Add slv.version argument to \_chk_other call.
- main:  Added slave configuration transpose data.
- run_program:  Added call to gen_libs.transpose_dict function, replaced cmds_gen.disconnect with mysql_libs.disconnect, process status connection on MySQL connection, and replaced cmds_gen.create_cfg_array with call to gen_libs.create_cfg_array.
- Removed unnecessary \*\*kwargs in function argument list.
- config/slave.txt.TEMPLATE: Added SSL configuration options.
- config/mongo.py.TEMPLATE:  Added SSL configuration options.
- config/mysql_cfg.py.TEMPLATE:  Added SSL configuration options.
- config/mysql.cfg.TEMPLATE:  Added SSL configuration options.
- Documentation updates.

## Removed
- cmds_gen module.

## [3.1.2] - 2020-11-23
- Updated to use the mysql_libs v5.0.3 library.
- Verified to work with pymongo v3.8.0.
- Updated to be used in FIPS 140-2 environment.
- Updated to work with (much older) mysql.connector v1.1.6 library module.

### Fixed
- chk_slv_err, \_process_time_lag:  Detected when mysql server is down.
- \_process_time_lag:  Detected when rep agent is down for -T option to standard out.
- chk_slv_err, chk_mst_log, \_chk_other, chk_slv_thr:  Fixed print formatting error.
- \_chk_other:  Fixed when slave instance is down.
- run_program:  Fixed disconnecting from down master/slave instance.
- run_program:  Corrected passing incorrect keyword argument for os_type.
- config/mysql.cfg.TEMPLATE:  Point to correct socket file.

### Changed
- \_process_json:  Captured and process status return from mongo_libs.ins_doc call.
- run_program:  Updated configuration names to match changes in configuration file.
- config/mongo.py.TEMPLATE:  Changed configuration entry and added a number of configuration entries.
- config/slave.txt.TEMPLATE:  Changed configuration entry and added a number of configuration entries.
- config/mysql_cfg.py.TEMPLATE:  Changed configuration entry.
- Documentation changes.


## [3.1.1] - 2020-05-21
### Fixed
- main: Fixed handling command line arguments from SonarQube scan finding.
- run_program:  Only disconnect from master when -c option is used.

### Added
- Added -f option to Flatten the JSON data structure to file and standard out.
- Added ProgramLock class to prevent multiple runs at the same time.
- Added global variable for template printing.
- Added -a option to allow for appending to output files.

### Changed
- run_program: Converted positional args to kwargs in mysql_class.MasterRep call.
- call_run_chk:  Changed variable name to standard naming convention.
- \_process_json:  Changed variable name to standard naming convention.
- chk_slv_err:  Changed variable name to standard naming convention.
- add_miss_slaves:  Changed variable name to standard naming convention.
- chk_mst_log: Replaced returning unused arguments into placeholders.
- call_run_chk:  Refactored "for" and "if" statements into a generator.
- \_process_json:  Added flattening of JSON structure to standard out and to file.
- call_run_chk:  Checked for "-f" option and passed JSON identation setting to functions.
- main:  Made "-s" option a requirement for "-A", "-C", "-D", "-E", "-O" and "-T" options.
- chk_slv_time:  Changed JSON document "Master" entry to "Server".
- add_miss_slaves:  Converted JSON document to PascalCase.
- chk_slv_time:  Converted JSON document to PascalCase.
- main:  Added ProgramLock class to implement program locking.
- main:  Made "-c" option a requirement for "-B", "-C", and "-T" options.
- \_chk_other: Used global variable for template printing.
- chk_slv: Used global variable for template printing.
- rpt_slv_log: Used global variable for template printing.
- chk_mst_log:  Removed unused code.
- chk_slv_thr: Used global variable for template printing.
- \_process_json:  Changed hardcoded write file mode to a variable to allow for write appending.
- call_run_chk:  Set file mode settings and passed to functions.
- config/mongo.py.TEMPLATE:  Changed format.
- config/mysql.cfg.TEMPLATE:  Changed format.
- config/mysql_cfg.py.TEMPLATE:  Changed format.
- config/slave.txt.TEMPLATE:  Changed format.
- Documentation updates.

### Removed
- Removed unused library modules.
- main:  Removed -f option which sets output as JSON or standard format.


## [3.1.0] - 2019-12-04
### Fixed
- chk_slv_time :  Capture time lag from \_process_time_lag function.
- \_process_time_lag:  Return updated time lag to calling function.

### Added
- Added -j option to change output to JSON format.  Uses a True|False setting instead of a string value.
- Added -z option to suppress standard out.

### Changed
- \_process_time_lag:  Replaced frmt with json_fmt.
- chk_slv_time: Added json_fmt to function and replaced frmt with json_fmt.
- call_run_chk:  Added -j option to function and replaced frmt with json_fmt.
- call_run_chk:  Replaced setup_mail with call to gen_class.setup_mail.
- \_process_json:  Added gen_libs.print_data call for JSON format.
- \_process_json:  Added suppress standard out option.
- call_run_chk:  Added suppress standard out option to function calls.
- Documentation update.

### Removed
- setup_mail:  Replaced by gen_class.setup_mail call.


## [3.0.0] - 2019-07-13
Breaking Change

- Modified program to use the mysql_class v4.0.0 version.  The v4.0.0 replaces the MySQLdb support library with the mysql.connector support library.

### Changed
- run_program:  Replaced section of code with call to mysql_libs.create_slv_array.
- chk_slv_time:  Replaced section of code with call to \_process_json.
- chk_slv_time:  Added capability to mail out JSON formatted data.
- call_run_chk:  Added setup of mail instance and passing mail instance to functions.
- main:  Added '-t' and '-u' options to allow for email capability for some options.
- chk_slv_time:  Replaced section of code with call to \_process_time_lag.
- chk_slv_time:  Removed "mongo_libs.json_prt_ins_2_db" and replaced with own internal code to do the same thing.
- chk_slv_other:  Replaced section of code with call to \_chk_other.
- call_run_chk:  Intersect args_array & func_dict to run options.
- main:  Refactored initial program checks.
- call_run_chk, run_program:  Added \*\*kwargs to argument list.
- Changed variable names to standard naming convention.
- add_miss_slaves, chk_slv_time:  Changed output to PascalCase.
- run_program:  Modified to use the updated mysql_class module.
- main:  Removed -I and -R arguments from the program options.
- run_program:  Replaced the code to load the slave files into an array with a call to cmds_gen.create_cfg_array().

### Removed
- Removed the imported modules os and gen_libs.errors.
- chk_rep:  No longer being implemented.
- rpt_srv_info:  No longer being implemented.

### Fixed:
- rpt_slv_log, chk_mst_log, chk_slv_thr, chk_slv_err, add_miss_slaves, chk_slv_time, chk_slv_other, call_run_chk, run_program, rpt_mst_log:  Fixed problem with mutable default arguments issue.
- 
### Added
- \_process_json:  Private function for chk_slv_time().  Process JSON data.
- setup_mail:  Initialize a mail instance.
- \_process_time_lag:  Private function for chk_slv_time().  Process time lag for slave.
- \_chk_other:  Private function for chk_slv_other().  Print any possible problems found.


## [2.0.1] - 2018-12-06
- Documentation updates.


## [2.0.0] - 2018-05-22
Breaking Change

### Changed
- Changed "mongo_libs" calls to new naming schema.
- Changed "mysql_class" calls to new naming schema.
- Changed "cmds_gen" calls to new naming schema.
- Changed "gen_libs" calls to new naming schema.
- Changed "arg_parser" calls to new naming schema.
- Changed function names from uppercase to lowercase.
- Setup single-source version control.


## [1.9.0] - 2018-05-16
### Changed
- Changed "cmds_mongo" to "mongo_libs" module reference.
- Changed "server" to "mysql_class" module reference.

### Added
- Added single-source version control.


## [1.8.0] - 2017-08-21
### Changed
- Call_Run_Chk:  Change MONGO_SVR to Mongo_Cfg to be standardized.
- Convert program to use local libraries from ./lib directory.
- Change single quotes to double quotes.
- Help_Message:  Replace docstring with printing the programs \_\_doc\_\_.


## [1.7.0] - 2016-11-04
### Fixed
- Chk_Mst_Log:  Corrected a formatting error and replaced two sections of code with call to Chk_Slv.

### Changed
- MySQL 5.6 (GTID Enabled) - Added GTID attributes to a number of functions.
- Rpt_Mst_Log:  Print master GTID position.
- Rpt_Slv_Log:  Print slave GTID information.
- Chk_Slv_Err:  Added IO and SQL error timestamps to output.

### Added
- Chk_Slv function.


## [1.6.0] - 2016-09-20
### Fixed
- Chk_Mst_Log:  Fixed error in if statement variable.

### Changed
- Run_Program:  Changed Setup_Class_Run_Chks to Run_Program to be inline with the other programs.  Changed -m to -c.  Added disconnect procedures for class instances.  Allow the -d option to be added to the -s file name if the -s does not include a path directory.
- main:  Changed the argument option values to be inline with the other programs.
- Call_Run_Chk:  Changed the argument option values to be inline with the other programs.
- Chk_Slv_Time:  Replaced a section of code with a library call to cmds_mongo.JSON_Prt_Ins_2_DB.


## [1.5.0] - 2016-09-15
### Changed
- Run_Program:  Converted port number from a string to an integer.  Being done in response to server.py V1.12 change to include port in all database connections.


## [1.4.0] - 2016-03-24
### Changed
- main:  Added "-b" and "-m" options and Added "-b" default value to variables.  Also added Arg_Cond_Req function to do a conditional requirement check on "-b" option.
- Chk_Slv_Time:  If "-b" option was selected then call a function to insert the JSON document into a Mongo database.
- Call_Run_Chk:  Get and process the "-b" and "-M" options.  Added named arguments to function calls and setup server configuration for Mongo database connection.


## [1.3.0] - 2016-03-21
### Changed
- Chk_Slv_Time:  Called function to add down slaves to JSON slave list.
- Add_Miss_Slaves:  Adds down/non-responding slave hosts to the JSON slave list.


## [1.2.0] - 2016-03-16
### Changed
- Setup_Class_Run_Chks:  Do not add slave instance to slave array if not able to connect to the database server.
- Modified a number of function calls and added "\*\*kwargs" to the argument list to allow the additional parameters for the "-f" and "-o" options to be passed.
- Main program:  Added sys.exit call.


## [1.1.0] - 2016-03-15
### Changed
- Chk_Slv_Time:  Setup new format as dictionary, printed out as normal or to the dictionary, converted the dictionary to JSON and then called Print_Data function to print the data to the correct output location (i.e. screen, file).
- Call_Run_Chk:  Processed the "-f" and "-o" options and passed them to the functions as named arguments (kwargs).
- main:  Added several new variables, replaced Arg_Parse with Arg_Parse2, reorganized the main 'if' statements and streamlined the check process, also added Arg_File_Chk function to the 'if' statement check.  Added two new options:  "-f" and "-o" for output format and output file respectively.
- Added new functionality to program to allow the Check Slave Lag Time function (Chk_Slv_Time) to print its output in JSON format.  This will be used to update a status web page.


## [1.0.0] - 2015-11-18
- Initial creation.

