#!/bin/bash

process_vitals() {

    echo "Generating critical alerts report..."
    echo "------------------------------------"

    mkdir -p reports

    grep "CRITICAL" active_logs/heart_rate_log.log | \
    awk -F'|' '{print $1"|"$2"|"$3}' \
    > reports/critical_alerts.txt

    grep "CRITICAL" active_logs/temperature_log.log | \
    awk -F'|' '{print $1"|"$2"|"$3}' \
    >> reports/critical_alerts.txt

    echo "Critical alerts were properly saved to reports/critical_alerts.txt"
}
water_audit() {

    echo "Water Usage Audit"

    awk -F'|' '
    /ICU_WATER_RESERVE/ {
        gsub(/^[ \t]+|[ \t]+$/, "", $3)
        sum += $3
        count++
    }
    END {
        if (count > 0)
            printf "Average ICU Water Usage: %.2f L/min\n", sum/count
        else
            printf "No ICU water records found\n"
    }' active_logs/water_usage_log.log
}
process_vitals


water_audit

echo "============================================"

echo "Hospital analysis completed successfully."

echo "Report generated: reports/critical_alerts.txt"

echo "These tasks were execution time: $(date)"

echo "============================================"
