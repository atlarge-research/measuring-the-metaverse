#!/bin/bash

adb push metabench_perfetto_config /data/misc/perfetto-configs

adb shell perfetto --txt -c /data/misc/perfetto-configs/metabench_perfetto_config \
    -o /data/misc/perfetto-traces/trace \
    --background
