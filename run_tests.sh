#!/bin/bash

cd tests
echo 'Starting Stress Test 1...'
python3 stress_test1.py
echo 'Finished Stress Test 1'

echo 'Starting Stress Test 2...'
python3 stress_test2.py
echo 'Finished Stress Test 2'

echo 'Starting Stress Test 3...'
python3 stress_test3.py
echo 'Finished Stress Test 3'

echo 'Starting Stress Test 4...'
python3 stress_test4.py
echo 'Finished Stress Test 4'

echo 'Starting Stress Test: Two clients make the same reservation simultaneously...'
python3 test_two_clients_same_reservation.py
echo 'Finished Stress Test'

echo 'All Stress Tests passed'