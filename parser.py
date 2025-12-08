import random
import json
import sys

def rollForDestroy(chance):
    """
    Returns a 1/chance chance. Returns true if the 1 in whatever succeeded.
    """
    num = random.randint(1,chance)
    return True if num==1 else False


def censorText(text, chance):
    """
    Censors a random selection of words in the given text by replacing their characters with spaces.

    Censors at a 1/chance chance. ie. if chance is 5, it's a 1/5 chance for any specific word to be deleted

    :param list text: A list of strings for the text
    """
    # split it into words
    # randomly remove a portion of the words

    for i in range(len(text)):
        if rollForDestroy(chance):
            # replace the word with x spaces, where x is the number of characters in the word
            word = " " * len(text[i])
            text[i] = word
    
    return text


def censorMetadata(metadata, iter, maxIter):
    # if it's the last one, replace them all with unknwon
    if iter == maxIter-1:
        metadata["title"] = "Unknown"
        metadata["artist"] = "Unknown"
        metadata["date"] = "Unknown"
        metadata["medium"] = "Unknown"

    else:
        # censor titles, artists, and mediums by randomly removing letters
        for field in ["title", "artist", "medium"]:
            newField = "" # new string to be put in metadata

            # for each character in the field, roll a destroy chance
            for i in range(len(metadata[field])):
                if rollForDestroy(maxIter-iter):
                    newField = newField + " "
                else:
                    newField = newField + metadata[field][i]
            
            metadata[field] = newField


        # censor date by randomly adjusting numbers a bit
        date = int(metadata["date"])

        # generate random one digit number, then multiply scale by how many times we've done it (varying a little around 10)
        date += random.randint(-9,+9) * random.randint(9,11)**(iter+1)
        metadata["date"] = str(date)



def generateEntry(text, metadata, iterations=3):
    """
    Generates an entry JSON object from text for a description and a dictionary for metadata
    """
    entry = {}
    # create an object to hold the data for each access. 0 will be the original without any censoring. The final one will be empty spaces for everything
    for i in range(0,iterations+1):
        entry[str(i)] = {}
    
    # do initial values
    entry["0"]["description"] = text
    entry["0"]["metadata"] = metadata.copy()

    # do text
    text = text.split()
    for i in range(iterations):
        # increase the chance of censoring each time. 1/4 -> 1/3 -> 1/2 -> 1/1 for 4 iterations
        text = censorText(text, iterations-i)
        entry[str(i+1)]["description"] = " ".join(text)

    # do metadata
    for i in range(iterations):
        censorMetadata(metadata, i, iterations)
        entry[str(i+1)]["metadata"] = metadata.copy()
    
    return entry


def doProcess():
    """
    Opens a space to paste, parses, and creates a JSON file based on the title.
    """
    metadata = {}
    metadata["title"] = sys.stdin.readline()[:-1]
    metadata["artist"] = sys.stdin.readline()[:-1]
    metadata["date"] = sys.stdin.readline()[:-1]
    metadata["medium"] = sys.stdin.readline()[:-1]
    metadata["citation"] = ""

    text = sys.stdin.readline()

    sys.stdin.close()
    title = metadata["title"]
    title = title.replace(" ", "_")

    entry = generateEntry(text, metadata)
    with open(title+".json", "w") as outfile:
        json.dump(entry, outfile, indent=4)
    
    # with open("entries.txt", "a") as outfile:
    #     outfile.write(title + "\n")


doProcess()