#!/bin/bash

. ./env.sh
echo $GLPATH
(exec fncs_broker 3 &> logs/broker.log &)
(exec fncs_player 24h step.player &> logs/player.log &)
(exec gridlabd TE_Challenge.glm &> logs/gridlabd.log &)
(export FNCS_CONFIG_FILE=TE_Challenge_agent.yaml && exec python3 Agent.py 86400 &> logs/agent.log &)