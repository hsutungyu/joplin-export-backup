from collections import defaultdict
import os
import requests
import shutil
import re
import sys

import cred
import pagination

# API Token for Joplin, stored in cred.py as JOPLIN_TOKEN = "<API token>"
JOPLIN_TOKEN = cred.JOPLIN_TOKEN
JOPLIN_API_URL = "http://localhost:41184"

PARAMS = dict()
PARAMS["token"] = JOPLIN_TOKEN
# need to provide this to a paginated API call
PARAMS["page"] = 1
PARAMS["fields"] = "id,parent_id,title,body"

def getFileOfResource(resourceID: str, filePath: str, params: dict) -> str:
    with requests.get(JOPLIN_API_URL + f"/resources/{resourceID}/file", params, stream=True) as r:
        with open(filePath + "/" + resourceID, "wb") as f:
            shutil.copyfileobj(r.raw, f)

def exportNotesInOneFolder(folderTitle: str):
    """export all notes in the given folder title in Joplin as .md format
    TODO: allows specifying the format of notes

    Args:
        folderTitle (str): the title of the folder to export all notes within
    """
    # folders do not have body
    allFolders = pagination.getAll(JOPLIN_API_URL + "/folders", {key: PARAMS[key] for key in PARAMS if key != "fields"})
    allNotes = pagination.getAll(JOPLIN_API_URL + "/notes", PARAMS)
    allResources = pagination.getAll(JOPLIN_API_URL + "/resources", {key: PARAMS[key] for key in PARAMS if key != "fields"})
    
    folderID = ""
    # remember each entry from getAll() is a page
    for page in allFolders:
        for folder in page:
            if folder["title"] == folderTitle:
                folderID = folder["id"]
                break
    
    if not folderID:
        raise KeyError("No folder with the given folder title is found. Please check your input.")
    
    # create a folder if not exists yet, do nothing if exists already
    os.makedirs(folderTitle.replace(" ", "_"), exist_ok=True)
    
    for page in allNotes:
        for note in page:
            if note["parent_id"] == folderID:
                # download the resources that this note should contain
                resourceIDRegex = r"!\[.*\]\(:/(.*)\)"
                resourcesInNote = re.findall(resourceIDRegex, note["body"])
                if resourcesInNote:
                    for resourceID in resourcesInNote:
                        getFileOfResource(resourceID, folderTitle.replace(" ", "_"), {key: PARAMS[key] for key in PARAMS if key == "token"})
                # fix path of resources that are referenced differently in Joplin
                note["body"] = re.sub(r"(!\[.*\])\(:/(.*)\)", r"\1(\2)", note["body"])
                # write a .md file
                with open(f'{folderTitle.replace(" ", "_")}/{note["title"].replace(" ", "_")}.md', "w", encoding="utf-16") as f:
                    f.write(note["body"])


if __name__ == "__main__":
    try:
        exportNotesInOneFolder(sys.argv[1])
    except IndexError:
        raise Exception("Please provide the name of the notebook that you want to backup.")
