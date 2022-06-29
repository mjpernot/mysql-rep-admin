# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [4.0.1] - 2022-06-29


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

