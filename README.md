# manga_notifier

A small python program that reads a file named 'Mangalist.txt' in the same directory in the following format separated by newlines

Berserk 357

Compares the name and chapters given in the list with the ones on https://mangadex.org which needs an account. Account 
settings should filter to the approriate language e.g. filter in english only if you read english translations.
Writes a log file with the current and laest chapter and sends the logfile.txt to an specified email. Credentials
and target email are to be provied in the config.py

Q: Why the use of a firefox profile?
A: Repeated log in depending on how often you set the script to run, would tick of the bot detection so I use an 
   firefox profile with an logged in account in mangadex.
   
Q: Why the unnecessary print?
A: Just used them for testing.

Q: Why the time.sleep(x)?
A: Same as first question. Website doesnt like too many quick requests.

Q: Can you give me your mangalist as an example?
A: No that is confidential ;)

Obviously this only works with manga that are up to date on mangadex.org.
