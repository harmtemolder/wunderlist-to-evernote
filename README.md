# Wunderlist to Evernote
A simple Python script that reformats a Wunderlist JSON export to an Evernote ENEX import

## Disclaimer
This thing is extremely rough around the edges. Feel free to adapt it to your own needs, but I can't be held responsible for any loss of data. Good luck.

## What does this do?
If you're migrating from Wunderlist to Evernote (like I was), this script translates your Wunderlist JSON export to an ENEX file that can then be imported in Evernote. It's based on these assumptions:
* Completed tasks aren't included in the ENEX file
* A task's notes and subtasks, if any, are added to the resulting note's content
* Completed subtasks of uncompleted tasks are included, but already checked
* A task's due date is added as a reminder date in the resulting note, but since Wunderlist doesn't save a due time, the time is set to 12h00 Zulu
* List names are added as a tag to notes

## How do I use it?
1. Go to [Wunderlist Account Settings](https://www.wunderlist.com/#/preferences/account)
2. Click `Create Backup` and, when it's finished creating your backup, `Click to Download`
3. Save the resulting JSON file next to wunderlist_to_evernote.py
4. Open your terminal
5. run `python wunderlist_to_evernote.py wunderlist-2019025-15_56_50.json`, replacing the JSON filename to your export, of course
6. Go to Evernote > File > Import Notes...
5. When importing in Evernote, don't forget to check "Import Tags" if you want to see your Wunderlist list names in Evernote

## What dependencies do I need to install?
```
pip install lxml pandas
```

## But how about [export.wunderlist.com](https://export.wunderlist.com/)?
I'm not sure, currently waiting on one of those. See [this](https://6wunderkinder.desk.com/customer/en/portal/articles/2364564-how-can-i-backup-export-my-data-) for more info.
