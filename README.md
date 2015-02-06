loghammer
=========

Log Hammer is a simple python-twisted based log collector built for scalability in the Cloud.

The simple Twisted process can be run in UDP (or TCP) mode and write log files to disk in chunks.
The chuck sizes are configurable.
Once the chunk is on disk we can use processing for example, uploading to S3 buckets. I have used boto for that purpose.


Why not write directly to S3?
I do not know if this is still tru but over an year ago there was no way to write async to S3 though you can perform parallel uploads. Its probably a limitation of HTTP interface itself. 



This system has been used in Production to collect TB of logs per day from multiple hosts without issues.


Inline processing by log lines
===
You cannot perform Inline processing for UDP mode of operation since complete lines are not logged. However in TCP mode you can perform additional async operation for every line.
