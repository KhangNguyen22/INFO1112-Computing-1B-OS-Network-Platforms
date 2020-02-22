#!/bin/bash

cd ../

# Connect Fail as IP address is rubbish
python3 client.py < tests/connect_fail.in | diff - ~/tests/connect_fail.out

if [ $? -eq "1" ]; then
	echo "Fail at test 1"
fi

# Connect Fail missing arguments. No port number

python3 client.py < tests/connect_missing_args.in | diff - ~/tests/connect_missing_args.out

if [ $? -eq "1" ]; then
	echo "Fail at test 2"
fi


# loginTest tests the ability to connect and login into server
python3 client.py < tests/login_test.in | diff - ~/tests/login_test.out

if [ $? -eq "1" ]; then
	echo "Fail at test 3"
fi


# login incomplete criteria
python3 client.py < tests/login_incomplete.in | diff - ~/tests/login_incomplete.out

if [ $? -eq "1" ]; then
	echo "Fail at test 4"
fi


# login invalid
python3 client.py < tests/login_invalid.in | diff - ~/tests/login_invalid.out

if [ $? -eq "1" ]; then
	echo "Fail at test 5"
fi

# observe 

python3 client.py < tests/observe.in |  diff - ~/tests/observe.out

if [ $? -eq "1" ]; then
	echo "Fail at test 6"
fi

# observe fail 

python3 client.py < tests/observe_fail.in |  diff - ~/tests/observe_fail.out

if [ $? -eq "1" ]; then
	echo "Fail at test 7"
fi

# move without arguments
python3 client.py < tests/move_without_args.in|  diff - ~/tests/move_without_args.out

if [ $? -eq "1" ]; then
	echo "Fail at test 8"
fi

# move west
python3 client.py < tests/move_west.in |  diff - ~/tests/move_west.out

if [ $? -eq "1" ]; then
	echo "Fail at test 9"
fi

# stats with args
python3 client.py < tests/stats_args.in |  diff - ~/tests/stats_args.out

if [ $? -eq "1" ]; then
	echo "Fail at test 10"
fi


# statTest tests the ability to connect,login into server and conduct stats command 
python3 client.py < tests/stat_test.in | diff - ~/tests/stat_test.out

if [ $? -eq "1" ]; then
	echo "Fail at test 11"
fi

# inspect south

python3 client.py < tests/inspect_south.in | diff - ~/tests/inspect_south.out

if [ $? -eq "1" ]; then
	echo "Fail at test 12"
fi

# inspect fail with hello

python3 client.py < tests/inspect_fail.in | diff - ~/tests/inspect_fail.out

if [ $? -eq "1" ]; then
	echo "Fail at test 13"
fi

# inspect missing arguments

python3 client.py < tests/inspect_missing.in | diff - ~/tests/inspect_missing.out

if [ $? -eq "1" ]; then
	echo "Fail at test 14"
fi

# note with no args

python3 client.py < tests/note_missing.in | diff - ~/tests/note_missing.out

if [ $? -eq "1" ]; then
	echo "Fail at test 15"
fi

# note hello

python3 client.py < tests/note.in | diff - ~/tests/note.out

if [ $? -eq "1" ]; then
	echo "Fail at test 16"
fi

# message missing arguments

python3 client.py < tests/message_missing.in | diff - ~/tests/message_missing.out

if [ $? -eq "1" ]; then
	echo "Fail at test 17"
fi

# message success

python3 client.py < tests/message.in  | diff - ~/tests/message.out

if [ $? -eq "1" ]; then
	echo "Fail at test 18"
fi

# commit fail too many args

python3 client.py < tests/commit_fail.in | diff - ~/tests/commit_fail.out

if [ $? -eq "1" ]; then
	echo "Fail at test 19"
fi

# commit success

python3 client.py < tests/commit.in | diff - ~/tests/commit.out

if [ $? -eq "1" ]; then
	echo "Fail at test 20"
fi

# # quit immediately
python3 client.py < tests/quit_instantly.in | diff - ~/tests/quit_instantly.out

 if [ $? -eq "1" ]; then
 	echo "Fail at test 21"
 fi

 # quit when connected

 python3 client.py < tests/quit_connect.in | diff - ~/tests/quit_connect.out

 if [ $? -eq "1" ]; then
 	echo "Fail at test 22"
 fi
