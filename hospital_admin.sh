#!/bin/bash

# Member 1: The Architect
initialize_system(){

     i="active_logs"
     a="archived_logs"
     r="reports"

  if [ -d "$i" ];
     then
       echo "file $i does exist"
  else
    echo "file doesn't exist; creating active_logs directory"
    mkdir "$i"
 fi

  if [ -d "$a" ];
     then
       echo "file $a does exist"
  else
   echo "file doesn't exist; creating archived_logs directory"
    mkdir "$a"
 fi

  if [ -d "$r" ];
     then
       echo "file $r does exist"
  else
    echo "file doesn't exist; creating reports directory"
    mkdir "$r"
 fi
}
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


initialize_system

secure_data
