#!/usr/local/bin/python
from datetime import datetime
import json
import os
import sys

from lxml import etree
import pandas as pd

def wunderlist_to_evernote(input_file, output_file):

    # Read tasks from Wunderlist export JSON file
    with open(input_file) as wunderlist_raw:
        wunderlist = json.load(wunderlist_raw)

    # Generate dict with list IDs and titles
    wl_lists = {}
    for list in wunderlist['data']['lists']:
        wl_lists[list['id']] = list['title']

    # Load tasks, subtasks and notes into dataframes
    wl_tasks = pd.DataFrame(wunderlist['data']['tasks'])
    wl_subtasks = pd.DataFrame(wunderlist['data']['subtasks'])
    wl_notes= pd.DataFrame(wunderlist['data']['notes'])

    # Only keep tasks that aren't completed yet
    wl_tasks = wl_tasks[wl_tasks['completed'] == False]

    # Loop through lists to create separate import files per list
    # for list_id, list_name in wl_lists.items():

    # Start filling an output ENEX tree with tasks from the Wunderlist list
    output_enex = etree.Element('en-export')

    # Loop through all tasks and process one by one
    for index, task in wl_tasks.iterrows():

        # Create a new note in the output XML's <en-export>
        note = etree.SubElement(output_enex, 'note')

        # Set the note's title to the task title
        title = etree.SubElement(note, 'title')
        title.text = task['title']

        # Set the note's created and updated dates to created_at
        date = datetime.strptime(
            task['created_at'],
            '%Y-%m-%dT%H:%M:%S.%fZ')  # in- and output are both in Zulu
        reformatted_date = date.strftime('%Y%m%dT%H%M%SZ')
        created = etree.SubElement(note, 'created')
        created.text = reformatted_date
        updated = etree.SubElement(note, 'updated')
        updated.text = reformatted_date

        # Add the note's due date to its title, if any
        if isinstance(task['due_date'], str):
            # Reformat Wunderlist's due date and set to 12h00 Zulu
            reminder = datetime.strptime(
                task['due_date'],
                '%Y-%m-%d').replace(hour=12)
            reformatted_reminder = reminder.strftime('%Y%m%dT%H%M%SZ')

            # Add <note-attributes> and <reminder-time>
            note_attributes = etree.SubElement(note, 'note-attributes')
            reminder_time = etree.SubElement(note_attributes, 'reminder-time')
            reminder_time.text = reformatted_reminder
            # TODO Does this work without <reminder-order>?

        # Create <content> within <note>
        content = etree.SubElement(note, 'content')

        # Create a separate <en-note> that will be added to <content>
        # within CDATA later
        en_note = etree.Element('en-note')

        # Look for the task's notes and subtasks, if any
        task_notes = wl_notes[wl_notes['task_id'] == task['id']]
        task_subtasks = wl_subtasks[wl_subtasks['task_id'] == task['id']]

        if len(task_notes) > 0:
            for index, row in task_notes.iterrows():
                # Add divs for every note found
                div = etree.SubElement(en_note, 'div')
                div.text = str(row['content'])

        if len(task_subtasks) > 0:
            for index, row in task_subtasks.iterrows():
                # Add divs for every subtask found
                div = etree.SubElement(en_note, 'div')

                # Add a checkbox that reflects the current completed state
                if row['completed'] == 'True':
                    checkbox = etree.SubElement(
                        div,
                        'en-todo',
                        {'checked': 'true'})
                else:
                    checkbox = etree.SubElement(
                        div,
                        'en-todo',
                        {'checked':'false'})

                # Add the subtask's title
                div.text = str(row['title'])
                # TODO For some reason the checkbox is placed behind the title

        # Add the <en-note> to <content> within CDATA
        content.text = etree.CDATA(etree.tostring(
            en_note,
            pretty_print=True,
            xml_declaration=True,
            encoding='ASCII',  # CDATA needs ASCII, apparently
            doctype='<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'))

        # Add the task's list as tag
        tag = etree.SubElement(note, 'tag')
        tag.text = wl_lists[task['list_id']]

    with open(output_file, 'wb') as enex_file:
        enex_file.write(etree.tostring(
            output_enex,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8',
            doctype='<!DOCTYPE en-export SYSTEM '
                    '"http://xml.evernote.com/pub/evernote-export3.dtd">'))


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        # i.e. if invoked without argument or not from terminal at all
        input_file = 'wunderlist-2019025-15_56_50.json'
        print('wunderlist_to_evernote.py: No input file entered, using '
              '{}'.format(
            input_file))
    else:
        # Assume that the first argument is the input file
        input_file = sys.argv[1]
        print('wunderlist_to_evernote.py: Using {} as input'.format(
            input_file))

    if not os.path.isfile(input_file):
        raise ValueError('The input file you entered doesn\'t exist. Check '
                         'your input and try again')

    output_file = 'evernote-{}.enex'.format(
        datetime.now().strftime('%Y%m%d-%H_%M_%S'))

    wunderlist_to_evernote(input_file, output_file)
