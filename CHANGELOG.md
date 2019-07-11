# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [3.0.0] - 2019-07-11
Breaking Change

- Modified program to use the mysql_class v4.0.0 version.  The v4.0.0 replaces the MySQLdb support library with the mysql.connector support library.

### Changed
- run_program:  Modified to use the updated mysql_class module.
- main:  Removed -I and -R arguments from the program options.
- run_program:  Modified to use the updated mysql_class module.
- run_program:  Replaced the code to load the slave files into an array with a call to cmds_gen.create_cfg_array().

### Removed
- Removed the imported module gen_libs.errors.
- chk_rep:  No longer being implemented.
- rpt_srv_info:  No longer being implemented.

### Fixed:
- rpt_mst_log:  Fixed problem with mutable default arguments issue.
- rpt_slv_log:  Fixed problem with mutable default arguments issue.
- chk_mst_log:  Fixed problem with mutable default arguments issue.
- chk_slv_thr:  Fixed problem with mutable default arguments issue.
- chk_slv_err:  Fixed problem with mutable default arguments issue.
- add_miss_slaves:  Fixed problem with mutable default arguments issue.
- chk_slv_time:  Fixed problem with mutable default arguments issue.
- chk_slv_other:  Fixed problem with mutable default arguments issue.
- call_run_chk:  Fixed problem with mutable default arguments issue.
- run_program:  Fixed problem with mutable default arguments issue.


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
### Changed
- MySQL 5.6 (GTID Enabled) - Added GTID attributes to a number of functions.
- Rpt_Mst_Log:  Print master GTID position.
- Rpt_Slv_Log:  Print slave GTID information.
- Chk_Mst_Log:  Corrected a formatting error and replaced two sections of code with call to Chk_Slv.
- Chk_Slv_Err:  Added IO and SQL error timestamps to output.

### Added
- Chk_Slv function.


## [1.6.0] - 2016-09-20
### Changed
- Run_Program:  Changed Setup_Class_Run_Chks to Run_Program to be inline with the other programs.  Changed -m to -c.  Added disconnect procedures for class instances.  Allow the -d option to be added to the -s file name if the -s does not include a path directory.
- main:  Changed the argument option values to be inline with the other programs.
- Call_Run_Chk:  Changed the argument option values to be inline with the other programs.
- Chk_Mst_Log:  Fixed error in if statement variable.
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

