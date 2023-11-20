#!/bin/bash

adb shell pkill perfetto

adb pull /data/misc/perfetto-traces/trace ./metabench_$(date +"%FT%T").ptrace

adb shell rm -f /data/misc/perfetto-traces/trace