#!/bin/bash

process_vitals() {

    echo "Generating critical alerts report..."

    mkdir -p reports

    grep "CRITICAL" active_logs/heart_rate.log | \
    awk -F',' '{print $1","$2","$3}' \
    > reports/critical_alerts.txt

    grep "CRITICAL" active_logs/temperature.log | \
    awk -F',' '{print $1","$2","$3}' \
    >> reports/critical_alerts.txt

    echo "Critical alerts saved to reports/critical_alerts.txt"
}
