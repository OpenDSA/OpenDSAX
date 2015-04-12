@echo off

REM This script will activate sdk virtual environment and then run xblock-sdk web server 
REM The script assumes that sdk virtualenv can be found in C:\envs\sdk
REM and xblock-sdk can be found in C:\dev\xblock-sdk

REM activate sdk virtualenv
call C:\envs\sdk\Scripts\activate.bat

REM run xblock-sdk web server
REM By default, the server runs on port 8000 on the IP address 127.0.0.1. 
REM You can pass in an IP address and port number explicitly.
cd C:\dev\xblock-sdk
call python manage.py runserver

:END