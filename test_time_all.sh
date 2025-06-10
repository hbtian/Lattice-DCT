#!/bin/bash

# 清空 logs 和 share 文件夹
rm -rf logs/*
rm -rf share/*
mkdir -p logs
mkdir -p share

# 写入CSV表头
echo "N,USER_ID,PEval_time,timezk,FinalEval_time,timevzk" > time_results.csv

for (( i=1; i<=15; i++ ))
do
    N=$((3 * i + 1))
    echo "Running PEval for N=$N ..."

    start=$(date +%s.%N)

    # 串行启动 worker 容器
    for (( j=1; j<=N; j++ ))
    do
        > logs/i${i}_user${j}.log
        echo "Running worker $j for N=$N ..."
        docker run --rm \
            -e USER_ID=$j \
            -e NUM_I=$i \
            -e ROLE=worker \
            -v "$(pwd)":/app \
            peval-sage-notebook >> logs/i${i}_user${j}.log 2>&1
    done

    # 等待所有 worker 完成
    wait

    echo "All PEval workers for N=$N finished."
    sleep 2

    echo "Running FinalEval..."
    > logs/i${i}_final.log
    docker run --rm \
        -e NUM_I=$i \
        -e ROLE=final \
        -v "$(pwd)":/app \
        peval-sage-notebook >> logs/i${i}_final.log 2>&1

    # 从日志中提取每个用户的时间数据并写入 CSV
    for (( j=1; j<=N; j++ ))
    do
        logfile="logs/i${i}_user${j}.log"
        PEval_time=$(grep "PEval:" "$logfile" | awk '{print $2}')
        timezk=$(grep "timezk" "$logfile" | awk '{print $2}')
        FinalEval_time=$(grep "FinalEval:" "logs/i${i}_final.log" | awk '{print $2}')
        timevzk=$(grep "timevzk" "logs/i${i}_final.log" | awk '{print $2}')

        echo "$N,$j,$PEval_time,$timezk,$FinalEval_time,$timevzk" >> time_results.csv
    done
done
