pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
        stage('Test') {
            steps {
                dir ('lib') {
                    git branch: "mod/294", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                dir ('mongo_lib') {
                    git branch: "mod/422", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/mongo-lib.git"
                }
                dir ('mongo_lib/lib') {
                    git branch: "mod/294", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                dir ('mysql_lib') {
                    git branch: "mod/532", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/mysql-lib.git"
                }
                dir ('mysql_lib/lib') {
                    git branch: "mod/294", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                sh """
                virtualenv test_env
                source test_env/bin/activate
                pip2 install mock==2.0.0 --user
                pip2 install mysql-connector-python==8.0.22 --user
                pip2 install psutil==5.4.3 --user
                pip2 install pymongo==3.8.0 --user
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
                deactivate
                rm -rf test_env
                """
            }
        }
        stage('SonarQube analysis') {
            steps {
                sh './test/unit/sonarqube_code_coverage.sh'
                sh 'rm -rf lib'
                sh 'rm -rf mongo_lib'
                sh 'rm -rf mysql_lib'
                script {
                    scannerHome = tool 'sonar-scanner';
                }
                withSonarQubeEnv('Sonar') {
                    sh "${scannerHome}/bin/sonar-scanner -Dproject.settings=sonar-project.JACIDM.properties"
                }
            
            }
        }
        stage('Artifactory upload') {
            steps {
                script {
                    server = Artifactory.server('Artifactory')
                    server.credentialsId = 'art-svc-highpoint-dev'
                    uploadSpec = """{
                        "files": [
                            {
                                "pattern": "./*.py",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-rep-admin/"
                            },
                            {
                                "pattern": "./*.txt",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-rep-admin/"
                            },
                            {
                                "pattern": "./*.md",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-rep-admin/"
                            },
                            {
                                "pattern": "*.TEMPLATE",
                                "recursive": true,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/mysql-rep-admin/config/"
                            }
                        ]
                    }"""
                    server.upload(uploadSpec)
                }
            }
        }
    }
    post {
        always {
            cleanWs disableDeferredWipeout: true
        }
    }
}
