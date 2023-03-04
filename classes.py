import datetime
import os
import subprocess
from pathlib import Path
import pandas as pd


def save():
    df.to_csv('df.csv', index=False, sep=';')
def create_df():
    try:
        df = pd.read_csv('df.csv', delimiter=';')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['tags', 'name', 'created', 'changed', 'note'])
    if os.path.exists('notes')==False:
        os.mkdir('notes')
    return df


df = create_df()

class Notebook(pd.DataFrame):
    def add_note(self, note):
        self.loc[len(self), ['name', 'created', 'note']] = [note.name.value, note.created, note]
        save()
    def change_note(self, note,changed=datetime.datetime.now().strftime('%m/%d/%Y, %H:%M')):
        self.loc[df['name'] == note.name.value, ['changed']] = changed
        save()

    def remove_note(self, note):
        self = self.loc[self['name'] != note.name.value]
        save()

class Field:
    def __init__(self, value):
        self._value = str(value)
        self.value = str(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    @Field.value.setter
    def value(self, value):
        try:
            fle = Path(f'./notes/{value}.txt')    #   .notes.{value}
            fle.touch(exist_ok=False)
            self.value = str(value)
        except FileExistsError:
            return f'Note with this name already exists'


class Tag(Field):
    @Field.value.setter
    def value(self, value):
        self.value = str(value)
        try:
            self.value = value.lower()
        except:
            pass


class Note():
    def __init__(self, name, tags='', created=datetime.datetime.now().strftime('%m/%d/%Y, %H:%M')):
        self.name = Name(name)
        self.tags = tags
        self.created = created


    def add_tags(self, new_tag):
        self.tags = new_tag
        df.loc[df['name'] == self.name.value, ['tags']] = self.tags



    def delete_tags(self):
        self.tags = ''
        df.loc[df['name'] == self.name.value, ['tags']] = ''

    def add_note(self):
        try:
            subprocess.call(['open', '-a', 'TextEdit', f'./notes/{self.name.value}.txt'])
            df.loc[len(df), ['name', 'created']] = [self.name.value, self.created]
        except:
            try:
                subprocess.call(['notepad', f'./notes/{self.name.value}.txt'])
                df.loc[len(df), ['name', 'created']] = [self.name.value, self.created]
            except FileNotFoundError:
                print("Text editor not found")

    def change_note(self, changed=datetime.datetime.now().strftime('%m/%d/%Y, %H:%M')):
        try:
            subprocess.call(['open', '-a', 'TextEdit', f'./notes/{self.name.value}.txt'])
            df.loc[df['name'] == self.name.value, ['changed']] = changed
        except:
            try:
                subprocess.call(['notepad', f'./notes/{self.name.value}.txt'])
                df.loc[df['name'] == self.name.value, ['changed']] = changed
            except FileNotFoundError:
                print("Text editor not found")

    def remove(self):
        global df
        os.remove(f'./notes/{self.name.value}.txt')
        df = df.loc[df['name'] != self.name.value]
        return df



def synk():
    global df
    names = os.listdir('notes')
    names = [i[:-4] for i in names]
    for name in names:
        if df['name'].isin([name]).any()==False:
            ex_note = Note(name)
            df.loc[len(df), ['name', 'created']] = [ex_note.name.value, ex_note.created]
    save()
    df = df.loc[df['name'].isin(names)==True]
    save()

synk()
