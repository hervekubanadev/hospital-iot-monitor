#!/bin/bash

initialize_system(){
     i="active_logs"
     a="archived_logs"
     r="reports"

  if [ -d "$i" ];
     then
       echo "file $i does exist"
  else
    echo "creating active_logs directory"
    echo $(mkdir $i)

 fi

  if [ -d "$a" ];
     then
       echo "file $a does exist"
  else
   echo "creating archived_logs directory"
    echo $(mkdir $a)

 fi

  if [ -d "$r" ];
     then
       echo "file $r does exist"
  else
    echo "creating reports directory"
    echo $(mkdir $r)

 fi
}
