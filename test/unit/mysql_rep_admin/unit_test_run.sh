#!/bin/bash
# Unit testing program for the program module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit testing..."
test/unit/mysql_rep_admin/add_miss_slaves.py
test/unit/mysql_rep_admin/call_run_chk.py
test/unit/mysql_rep_admin/chk_mst_log.py
test/unit/mysql_rep_admin/chk_slv.py
test/unit/mysql_rep_admin/chk_slv_err.py
test/unit/mysql_rep_admin/chk_slv_other.py
test/unit/mysql_rep_admin/chk_slv_thr.py
test/unit/mysql_rep_admin/chk_slv_time.py
test/unit/mysql_rep_admin/help_message.py
test/unit/mysql_rep_admin/main.py
test/unit/mysql_rep_admin/rpt_mst_log.py
test/unit/mysql_rep_admin/rpt_slv_log.py
test/unit/mysql_rep_admin/run_program.py
