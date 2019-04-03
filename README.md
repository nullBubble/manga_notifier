# manga_notifier

A small python program that reads a file named 'Mangalist.txt' in the same directory separated by newlines in the following format

Berserk 357

The full name like on mangadex must be written in the Mangalist.txt

Compares the chapters given in the list with the ones on https://mangadex.org which needs an account. Account 
settings should filter to the approriate language e.g. filter in english only if you read english translations.
Writes a log file with the current and laest chapter and sends the logfile.txt to an specified email. Credentials
and target email are to be provided in the config.py
The sender email account must allow the use of less secure apps for this send_mail method to work.

Q: Why the use of a firefox profile?

A: Repeated log in depending on how often you set the script to run, would tick off the bot detection so I use an 
   firefox profile with an alraedy logged in account in mangadex.
   
Q: Why the unnecessary prints?

A: Just used them for testing.

Q: Why the time.sleep(x)?

A: Same as first question. Website doesnt like too many quick requests.

Q: Can you give me your mangalist as an example?

A: No that is confidential ;)

Obviously this only works with manga that are up to date on mangadex.org.
