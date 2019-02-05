# Wunderlist to Evernote
A simple Python script that reformats a Wunderlist JSON export to an Evernote ENEX import

## What does this do?
If you're migrating from Wunderlist to Evernote (like I was), this script translates your Wunderlist export to an ENEX file that can then be imported in Evernote. It's set up like this:
* Completed tasks aren't included in the ENEX file
* Completed subtasks of uncompleted tasks are included
* A task's notes and subtasks, if any, are added to the resulting note's content
* A task's due date is added as a reminder date in the resulting note
* ...

## How do I use it?
1. Go to [Wunderlist Account Settings](https://www.wunderlist.com/#/preferences/account)
2. Click `Create Backup` and, when it's finished creating your backup, `Click to Download`
3. Save the resulting JSON file next to wunderlist_to_evernote.py
4. ...

## But how about [export.wunderlist.com](https://export.wunderlist.com/)?
I'm not sure, currently waiting on one of those. See [this](https://6wunderkinder.desk.com/customer/en/portal/articles/2364564-how-can-i-backup-export-my-data-) for more info.