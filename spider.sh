#! /bin/bash
pidof l1.py
while [ $? -ne 0 ]
do 
    echo "Process exits with errs ! Restarting!"
    python3 l1.py
done 
echo "Process ends!"
