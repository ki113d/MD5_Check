MD5_Check
=========

A simple command line tool to check md5 hashes against online databases. This application was originally written to find cleartext passwords from user password dumps.


Usage:
------
~~~
usage: md5ch.py [-h] [-d DELAY] [-s] in_file out_file

positional arguments:
  in_file               File from which the hashes should be read.
  out_file              File to which the discovered hashes should bewritten.

optional arguments:
  -h, --help            show this help message and exit
  -d DELAY, --delay DELAY
                        Delay in seconds, between each hash check.
  -s, --single          With this parameter each line should consist of a lone
                        md5 hash!
~~~

Input file format rules:
------------------------
Input files can be in either one of the following formats.

###Normal mode:
Each line should consist of a username hash pair separated by a single colon and no whitespace.
####Example:
~~~
ki113d:f84315fdf36e0ff0da874d8a5728d337
~~~
will be written to the output file as:
~~~
ki113d:python
~~~

###Single mode:
Single mode requires the single parameter and each md5 hash must be on it's own line.
####Example:
~~~
23eeeb4347bdd26bfc6b7ee9a3b755dd
~~~
will be written to the output file as:
~~~
23eeeb4347bdd26bfc6b7ee9a3b755dd = python
~~~

Todo
----
- [X] Basic code done.
- [ ] Add Windows colouring support.
- [ ] Add the ability to add multiple servers through a config file.


Screenshot:
-----------
![Screenshot](http://i.imgur.com/pCUQ6bN.png?1)
