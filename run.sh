#!/bin/bash

. ./env.sh

(exec fncs_broker 3 &> logs/broker.log &)
(exec fncs_player 4h step.player &> logs/player.log &)
(exec gridlabd TE_Challenge.glm &> logs/gridlabd.log &)
(export FNCS_CONFIG_FILE=TE_Challenge_agent.yaml && exec python3 Agent.py 14400 &> logs/agent.log &)