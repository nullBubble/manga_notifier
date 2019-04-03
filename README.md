# manga_notifier

A small python program that reads a file named 'Mangalist.txt' in the format 'Name Chapter' with entries separated by new lines.
Compares the provided manga and chapter with the ones one https://mangadex.org and writes a log file called 'log.txt' with the 
current and latest chapter. This logfile gets sent via email to your provided email address. Sender email account credentails
and receiver email address are in the config.py
