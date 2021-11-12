Hello!

MailCorgi is built as a replacement for Maildog, Hack Club's legacy Airtable/Zapier powered bot for Hack Club Mail Team. 

MailCorgi is written in python, using Supabase as a database. 

MailCorgi requires a supabase db set up. You can probably figure out how the tables look like by looking at the code, but I'll be happy to dig up the table and column names out, should you need it.
This project is a WIP. It is jumbled together to the point where I don't know how it works. It has nearly 0 code comments, and you may have a hard time figuring out what's happening.

Mailcorgi requires these python packages(available via pip)
shippo, supabase_py, slack-bolt, and reportlab.

Early on, I discovered a case where the application had a critical error(don't remember), but uninstall dataclasses, that will fix the issue.

supabase has a default address return of 1000. When you have more than that many(I have ~12K), it will not return all and can lead to undefined behavior(record is there, not being found because it's not being returned). To fix, go to your project dashboard > Settings > API > Record Return #. This is still pretty fast

Currently on v0.0.3
Latest Update: adds address modal prefill 11/12/2021



