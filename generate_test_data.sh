#!/bin/bash
echo "Generating test data for dashboard..."
echo '{"message": "Failed password for root from 8.8.8.8 port 22 ssh2"}' | nc localhost 5044
echo '{"message": "Accepted password for admin from 192.168.1.100 port 22 ssh2"}' | nc localhost 5044
echo '{"message": "Failed password for user from 10.0.0.5 port 22 ssh2"}' | nc localhost 5044
echo '{"message": "Failed password for test from 1.1.1.1 port 22 ssh2"}' | nc localhost 5044
echo '{"message": "Accepted password for guest from 172.16.1.50 port 22 ssh2"}' | nc localhost 5044
echo "Test data generated! Aishat can now query real data."
