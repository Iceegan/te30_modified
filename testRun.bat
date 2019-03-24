set FNCS_FATAL=yes
set FNCS_LOG_STDOUT=yes
set FNCS_LOG_LEVEL=
set FNCS_TRACE=no
set FNCS_TIME_DELTA=

set FNCS_CONFIG_FILE=
start /b cmd /c fncs_broker 2 ^>broker.log 2^>^&1

set FNCS_CONFIG_FILE=TE_Challenge_testAgent.yaml
start /b cmd /c python testAgent.py 86400 ^>testRun.log 2^>^&1

set FNCS_CONFIG_FILE=
set FNCS_LOG_LEVEL=
set FNCS_LOG_STDOUT=yes
start /b cmd /c gridlabd -D USE_FNCS -D METRICS_FILE=TE_Challenge_metrics.json TE_Challenge.glm ^>gridlabd.log 2^>^&1
