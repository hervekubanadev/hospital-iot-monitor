#!/bin/bash

secure_data() {

    echo "============================================"
    echo "  Securing active_logs directory..."
    echo "============================================"

    chmod 700 active_logs

    echo "Permissions applied: Owner-only access."

    echo ""
    echo "Current permissions:"
    ls -ld active_logs
}
