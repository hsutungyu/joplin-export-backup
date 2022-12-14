# joplin-export-backup
A Python utility that exports and backup notes as Markdown format in [Joplin](https://joplinapp.org/) to a Cloud Storage bucket of Google Cloud.

## Note
The utility changes the markdown notes. Specifically, two things are changed:<br>
1. the local links to images and other resources are changed because of how Joplin stores the resources internally.
For example, if you insert an image `test.png` to a note in Joplin, then Joplin would create a link `![test.png](:/<an internal ID generated by Joplin)` within your notes.<br>
This script modify the link to remove `:/` such that the notes can be used within any local filesystem.<br>
2. the spaces within the filename are changed to underscores<br>

Therefore, the notes exported by this utility **cannot** be re-imported to Joplin.<br>
If you want to backup the notes but re-import them to Joplin, use the built-in backup or export functions instead.

## How to use the utility
1. In Joplin, open Tools -> Options -> Web Clipper
2. Click "Enable Web Clipper Service"
3. Click "Copy Token" to get the Joplin API token
4. create `cred.py` in the cloned repository, its content should look like:
```
JOPLIN_TOKEN = "<the API token that you copied>"
```
5. run `py main.py <name of the notebook that you want to backup>`<br>
For example, if we want to backup all notes within the notebook "Testing Testing", then run:<br>
`py main.py "Testing Testing"` (remember the quotes)

## Output
The utility creates a folder with the name same as the name of the notebook.<br>
Inside the folder, all the notes and the resources (e.g., images) within the notes are exported to the folder.

## TODO
- rewrite the utility as a Joplin plugin
- rewrite the utility to backup the whole Joplin