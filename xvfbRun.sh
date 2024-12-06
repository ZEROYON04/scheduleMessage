#!/bin/bash

# 関数定義: scheduleMessage.pyを停止
stop_schedule_message() {
    pids=$(pgrep -f scheduleMessage.py)
    if [ -n "$pids" ]; then
        echo "Stopping running instances of scheduleMessage.py."
        kill -9 $pids
    else
        echo "No running instances of scheduleMessage.py found."
    fi
}

# 関数定義: scheduleMessage.pyを開始
start_schedule_message() {
    echo "Starting xvfb-run."
    nohup xvfb-run -a python -u scheduleMessage.py &
}

# 引数の解析
ACTION=$1

# 引数に応じた動作
if [ -z "$ACTION" ]; then
    # 引数がない場合はrestartの動作
    stop_schedule_message
    start_schedule_message
else
    case $ACTION in
        start)
            start_schedule_message
            ;;
        stop)
            stop_schedule_message
            ;;
        restart)
            stop_schedule_message
            start_schedule_message
            ;;
        *)
            echo "Usage: $0 {start|stop|restart}"
            exit 1
            ;;
    esac
fi