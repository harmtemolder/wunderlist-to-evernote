from datetime import datetime
import json
import xml.etree.ElementTree as ET

import pandas as pd

if __name__ == '__main__':
    # Read tasks from Wunderlist export JSON file
    input_file = 'wunderlist-2019025-13_44_06.json'
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
    for list_id, list_name in wl_lists.items():
        output_file = '{} - Evernote Import - {}.enex'.format(
            datetime.now().strftime('%Y%m%d'),
            list_name
        )

        # Start filling an output XML with tasks from the Wunderlist list
        output_xml = ET.Element('en-export')

        list_tasks = wl_tasks[wl_tasks['list_id'] == list_id]

        # Loop through all tasks for this list
        for index, task in list_tasks.iterrows():
            # Create a new note in the output XML
            note = ET.SubElement(output_xml, 'note')

            # Set the note's title to the task title
            title = ET.SubElement(note, 'title')
            title.text = task['title']

            # Set the note's created and updated dates to created_at
            date = datetime.strptime(
                task['created_at'],
                '%Y-%m-%dT%H:%M:%S.%fZ')  # in- and output are in Zulu time
            reformatted_date = date.strftime('%Y%m%dT%H%M%SZ')
            created = ET.SubElement(note, 'created')
            created.text = reformatted_date
            updated = ET.SubElement(note, 'updated')
            updated.text = reformatted_date

            # Add the note's due date to its title, if any
            if isinstance(task['due_date'], str):
                title.text = 'Voor {}: {}'.format(
                    task['due_date'],
                    title.text)

            # Look for the task's notes and subtasks, if any
            task_notes = wl_notes[wl_notes['task_id'] == task['id']]
            task_subtasks = wl_subtasks[wl_subtasks['task_id'] == task['id']]

            content = ET.SubElement(note, 'content')
            en_note = ET.SubElement(content, 'en-note')

            notes_subtasks = []
            if len(task_notes) > 0:
                for index, row in task_notes.iterrows():
                    notes_subtasks.append(str(row['content']))
            if len(task_subtasks) > 0:
                for index, row in task_subtasks.iterrows():
                    notes_subtasks.append(str(row['title']))
            if len(notes_subtasks) > 0:
                en_note.text = '<br \>'.join(notes_subtasks)

        # Write to ENEX file
        output_enex = ET.ElementTree(output_xml)
        output_enex.write(output_file)
