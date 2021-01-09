# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Jean Bizot <jean@styckr.io>
""" Main lib for charles_package Project
"""

from os.path import split
import pandas as pd
import datetime

pd.set_option('display.width', 200)


def clean_data(data):
    """ clean data
    """
    # Remove columns starts with vote
    cols = [x for x in data.columns if x.find('vote') >= 0]
    data.drop(cols, axis=1, inplace=True)
    # Remove special characteres from columns
    data.loc[:, 'civility'] = data['civility'].replace('\.', '', regex=True)
    # Calculate Age from day of birth
    actual_year = datetime.datetime.now().year
    data.loc[:, 'Year_Month'] = pd.to_datetime(data.birthdate)
    data.loc[:, 'Age'] = actual_year - data['Year_Month'].dt.year
    # Uppercase variable to avoid duplicates
    data.loc[:, 'city'] = data['city'].str.upper()
    # Take 2 first digits, 2700 -> 02700 so first two are region
    data.loc[:, 'postal_code'] = data.postal_code.str.zfill(5).str[0:2]
    # Remove columns with more than 50% of nans
    cnans = data.shape[0] / 2
    data = data.dropna(thresh=cnans, axis=1)
    # Remove rows with more than 50% of nans
    rnans = data.shape[1] / 2
    data = data.dropna(thresh=rnans, axis=0)
    # Discretize based on quantiles
    data.loc[:, 'duration'] = pd.qcut(data['surveyduration'], 10)
    # Discretize based on values
    data.loc[:, 'Age'] = pd.cut(data['Age'], 10)
    # Rename columns
    data.rename(columns={'q1': 'Frequency'}, inplace=True)
    # Transform type of columns
    data.loc[:, 'Frequency'] = data['Frequency'].astype(int)
    # Rename values in rows
    drows = {1: 'Manytimes', 2: 'Onetimebyday', 3: '5/6timesforweek',
             4: '4timesforweek', 5: '1/3timesforweek', 6: '1timeformonth',
             7: '1/trimestre', 8: 'Less', 9: 'Never'}
    data.loc[:, 'Frequency'] = data['Frequency'].map(drows)
    return data


def try_me():
    print('Enter your name:')
    x = input()
    print(f"Pikaboo {x}!")
    for i in range(3):
        print()
    print(f"I'm sure you didn't see that coming {x}!")
    for i in range(5):
        print()
    print("Enter your name (and don't mispell it):")
    y = input()
    if y != x:
        print(f"Hum... Nice to meet you {y}")
        print(f"How many more personalities do you have?:")
        n = input()
        if type(n) not int:
            print(f"How many more personalities do you have? (enter a number please...):")
            n = input()
        if n == 0:
            print(f"Good, life is complicate enough like this, ahah")
        else:
            print(f"Sorry {y}, but I don't have time for that")
    for i in range(15):
        print()
    print("... Neither that!")
    for i in range(5):
        print()
    print("*enjoying this divine feeling of satisfaction*")
    for i in range(4):
        print()
    print(f"Do you want more? (y/n)")
    a = input()
    if a == 'y':
        for i in range(5):
            print()
        print(f"Well, {y}, you are living dangerously...")
        for i in range(5):
            print()
        if y != None:
            print(f"I'm not sure {x} would like that..")
            for i in range(2):
                print("...")
            print("Anyway...")
            for i in range(2):
                print("...")
            print(f"{y} Here is your reward:")
            print("'Mental breakdown is when you call your own bluff'")
            print("@fakeBaudrillard")
            print("[not me by the way, I'm just a fan]")
    else:
        print("Too bad you missed the reward..")
        if y == None:
            print("...and an alternate path... ;)")
        print("You should try_me() again [lol, going meta]")





if __name__ == '__main__':
    # For introspections purpose to quickly get this functions on ipython
    import charles_package
    folder_source, _ = split(charles_package.__file__)
    df = pd.read_csv('{}/data/data.csv.gz'.format(folder_source))
    clean_data = clean_data(df)
    print(' dataframe cleaned')
