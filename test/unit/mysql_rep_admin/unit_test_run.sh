#!/bin/bash
# Unit testing program for the program module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit testing..."
/usr/bin/python ./test/unit/mysql_rep_admin/add_miss_slaves.py
/usr/bin/python ./test/unit/mysql_rep_admin/call_run_chk.py
/usr/bin/python ./test/unit/mysql_rep_admin/chk_mst_log.py
/usr/bin/python ./test/unit/mysql_rep_admin/chk_other.py
/usr/bin/python ./test/unit/mysql_rep_admin/chk_slv.py
/usr/bin/python ./test/unit/mysql_rep_admin/chk_slv_err.py
/usr/bin/python ./test/unit/mysql_rep_admin/chk_slv_other.py
/usr/bin/python ./test/unit/mysql_rep_admin/chk_slv_thr.py
/usr/bin/python ./test/unit/mysql_rep_admin/chk_slv_time.py
/usr/bin/python ./test/unit/mysql_rep_admin/data_out.py
/usr/bin/python ./test/unit/mysql_rep_admin/dict_out.py
/usr/bin/python ./test/unit/mysql_rep_admin/help_message.py
/usr/bin/python ./test/unit/mysql_rep_admin/is_time_lag.py
/usr/bin/python ./test/unit/mysql_rep_admin/main.py
/usr/bin/python ./test/unit/mysql_rep_admin/process_time_lag.py
/usr/bin/python ./test/unit/mysql_rep_admin/rpt_mst_log.py
/usr/bin/python ./test/unit/mysql_rep_admin/rpt_slv_log.py
/usr/bin/python ./test/unit/mysql_rep_admin/run_program.py
