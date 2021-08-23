#!/bin/bash
# Unit test code coverage for SonarQube to cover all modules.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#       that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/add_miss_slaves.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/call_run_chk.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/chk_mst_log.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/chk_other.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/chk_slv.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/chk_slv_err.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/chk_slv_other.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/chk_slv_thr.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/chk_slv_time.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/help_message.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/main.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/process_json.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/process_time_lag.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/rpt_mst_log.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/rpt_slv_log.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/run_program.py
coverage run -a --source=mysql_rep_admin test/unit/mysql_rep_admin/transpose_dict.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
coverage xml -i
