#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import tkinter as tk
from gingerit.gingerit import GingerIt
import sys
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
import json

root = tk.Tk()
root.title('LivingSky Tech Grammar Check')
root.geometry('800x600+100+50')

text = tk.Text(root, width=40, height=30)
text.place(x=50, y=50)


def retrieve_input():
    input = text.get('1.0', 'end-1c')
    return input


class ColoredText:

    """Colored text class"""

    colors = [
        'black',
        'red',
        'green',
        'orange',
        'blue',
        'magenta',
        'cyan',
        'white',
        ]
    color_dict = {}
    for (i, c) in enumerate(colors):
        color_dict[c] = (i + 30, i + 40)

    @classmethod
    def colorize(
        cls,
        text,
        color=None,
        bgcolor=None,
        ):
        """Colorize text
        @param cls Class
        @param text Text
        @param color Text color
        @param bgcolor Background color
        """

        c = None
        bg = None
        gap = 0
        if color is not None:
            try:
                c = cls.color_dict[color][0]
            except KeyError:
                print ('Invalid text color:', color)
                return (text, gap)

        if bgcolor is not None:
            try:
                bg = cls.color_dict[bgcolor][1]
            except KeyError:
                print ('Invalid background color:', bgcolor)
                return (text, gap)

        (s_open, s_close) = ('', '')
        if c is not None:
            s_open = '' % c
            gap = len(s_open)
        if bg is not None:
            s_open += '' % bg
            gap = len(s_open)
        if not c is None or bg is None:
            s_close = ''
            gap += len(s_close)
        return ('%s%s%s' % (s_open, text, s_close), gap)


def get_ginger_url(text):
    """Get URL for checking grammar using Ginger.
    @param text English text
    @return URL
    """

    API_KEY = '6ae0c3a0-afdc-4532-a810-82ded0054236'

    scheme = 'http'
    netloc = 'services.gingersoftware.com'
    path = '/Ginger/correct/json/GingerTheText'
    params = ''
    query = urllib.parse.urlencode([('lang', 'US'), ('clientVersion',
                                   '2.0'), ('apiKey', API_KEY), ('text'
                                   , text)])
    fragment = ''

    return urllib.parse.urlunparse((
        scheme,
        netloc,
        path,
        params,
        query,
        fragment,
        ))


def get_ginger_result(text):
    """Get a result of checking grammar.
    @param text English text
    @return result of grammar check by Ginger
    """

    url = get_ginger_url(text)

    try:
        response = urllib.request.urlopen(url)
    except HTTPError as e:
        print ('HTTP Error:', e.code)
        quit()
    except URLError as e:
        print ('URL Error:', e.reason)
        quit()

    try:
        result = json.loads(response.read().decode('utf-8'))
    except ValueError:
        print ('Value Error: Invalid server response.')
        quit()

    return result


def main():
    text3 = tk.Text(root, width=40, height=30)
    text3.place(x=500, y=50)
    text3.tag_config('a', background='#FFD2D2', foreground='red')
    original_text = text.get('1.0', 'end-1c')
    if len(original_text) > 600:
        text3.insert(tk.END,
                     "You can't check more than 600 characters at a time."
                     )
    fixed_text = original_text
    results = get_ginger_result(original_text)

    # Incorrect grammar

    (color_gap, fixed_gap) = (0, 0)


    lastSuggestIndex = 0
    for result in results['LightGingerTheTextResult']:
        if result['Suggestions']:
            from_index = result['From'] + color_gap
            to_index = result['To'] + 1 + color_gap
            suggest = result['Suggestions'][0]['Text']

            # Colorize text


            colored_incorrect = ColoredText.colorize(original_text[from_index:to_index])[0]
            (colored_suggest, gap) = ColoredText.colorize(suggest)

            original_text = original_text[:from_index] + colored_incorrect + original_text[to_index:]

            fixed_text = fixed_text[:from_index - fixed_gap] + colored_suggest + fixed_text[to_index - fixed_gap:]


            nonColoredText = fixed_text[lastSuggestIndex:from_index - fixed_gap]
            fixed_gap += to_index - from_index - len(suggest)



            # add non-colored text from the end of the last suggest (or 0 on the first time) to the start of the current suggest :
            
            if len(nonColoredText) > 0 :
                if from_index != 0 and nonColoredText[-1] != "\n" :
                    text3.insert(tk.END, nonColoredText + " ")
                else :
                    text3.insert(tk.END, nonColoredText)
			# add colored suggest :
            text3.insert(tk.END, colored_suggest, 'a')
			# update end of last suggest :
            lastSuggestIndex = to_index - fixed_gap
			#just in case :
            if lastSuggestIndex < 0 :
                lastSuggestIndex = 0
            

	# we reached the end of suggestions	so now we add the remaining text
    text3.insert(tk.END, fixed_text[lastSuggestIndex:])

def combine_funcs(*funcs):

    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return combined_func


myButton1 = tk.Button(text='enter', command=combine_funcs(main,
                      lambda : retrieve_input()))
myButton1.place(x=400, y=300)

root.mainloop()


			