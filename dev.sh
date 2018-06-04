#!/bin/bash


# sigint_handler()
# {
#     echo 'handle sigint'
#     kill -s SIGINT $srv_pid
#     wait $srv_pid
# }

# python static_server.py &
# srv_pid=$!
# echo 'here'
# echo $srv_pid

# trap sigint_handler SIGINT

# FLASK_APP=src/martini.py FLASK_DEBUG=1 flask run

sigint_handler()
{
    echo 'handle sigint';
    kill $srv_pid;
    echo 'done done';
}

python static_server.py &
srv_pid=$!
trap sigint_handler SIGINT
FLASK_APP=src/martini.py FLASK_DEBUG=1 flask run
wait $srv_pid;
