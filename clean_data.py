from numpy import NaN
import pandas as pd

#df = pd.read_csv('./data/problem_data_lc.csv')
df = pd.read_csv('./data/problem_data_codeforces.csv')

def clean_cf_tags(df):
    df['tags'] = df['tags'].str.replace('+', ' ') #replace + with space
    df['tags'] = df['tags'].str.replace("'", '') #strip single quotes
    df['tags'] = df['tags'].str.slice(1,-1) #strip op, end brackets

def clean_cf_descs(df):
    df['description'] = df['description'].str.replace(r'<.+?>', '', regex=True) #strip all html tags
    df['description'] = df['description'].str.replace("<div class=\"", '') #manually strip this ending sequence
    df['description'] = df['description'].str.replace('&nbsp;', ' ') #convert html space
    df['description'] = df['description'].str.replace('&lt;', '<') #convert <, >, <=, >=
    df['description'] = df['description'].str.replace('&gt;', '>')
    df['description'] = df['description'].str.replace('&le;', '<=')
    df['description'] = df['description'].str.replace('&ge;', '>=')

clean_cf_tags(df)
clean_cf_descs(df)
df.to_csv('./data/cleaned_data_codeforces.csv')

def clean_tags(df):
    def clean_tag_apply(x):
        try:
            return x['topics'][x['topics'].find('>'):]
        except:
            return NaN
    def misc(x):
        try:
            if x['topics'].find('<') != -1:
                return x['topics'][:x['topics'].find('<')]
            return x['topics']
        except:
            return NaN
    df['topics'] = df.apply(lambda x: clean_tag_apply(x), axis=1)
    #df['topcs'] = df['topics'].str.slice(df['topics'].str.find('>')) #remove beginning garbage
    df['topics'] = df['topics'].str.replace(r'<span.+?>', ', ', regex=True) #add space between tags
    df['topics'] = df['topics'].str.replace(r'<.+?>', '', regex=True) #strip all other html tags
    df['topics'] = df['topics'].str.replace('&nbsp;', ' ') #convert html space
    df['topics'] = df['topics'].str.slice(2, -1) #trimming some misc <'s
    df['topics'] = df.apply(lambda x: misc(x), axis=1)
    df = df.replace('<timed out, manual entry>', NaN) #replace unparsed runtimes


def clean_descriptions(df):
    df['description'] = df['description'].str.slice(4) #strip begin div
    df['description'] = df['description'].str.replace(r'<.+?>', '', regex=True) #strip all html tags
    df['description'] = df['description'].str.replace('&nbsp;', ' ') #convert html space
    df['description'] = df['description'].str.replace('&lt;', '<') #convert <, >, <=, >=
    df['description'] = df['description'].str.replace('&gt;', '>')
    df['description'] = df['description'].str.replace('&le;', '<=')
    df['description'] = df['description'].str.replace('&ge;', '>=')
    # Remove all examples, but include constraints if it is there
    def trim_examples(x):
        if x['description'].find('Example 1') != -1:
            if x['description'].find('Constraints') != -1:
                return x['description'][0 : x['description'].find('Example 1')] + x['description'][x['description'].find('Constraints') :]
            return x['description'][0 : x['description'].find('Example 1')]
        return x

    df['description'] = df.apply(lambda x: trim_examples(x), axis=1)
    df['description'] = df.apply(lambda x: x['description'][:-2], axis=1)


'''
df['description'] = df['description'].str.slice(4) #strip begin div
df['description'] = df['description'].str.replace('<p>', '') #strip all p tags
df['description'] = df['description'].str.replace('</p>', '') #strip all p tags
df['description'] = df['description'].str.replace('<code>', '') #strip all code tags
df['description'] = df['description'].str.replace('</code>', '') #strip all code tags
df['description'] = df['description'].str.replace('&nbsp;', ' ') #convert html space
df['description'] = df['description'].str.replace(r'<a.+?>', '') #strip all a tags
df['description'] = df['description'].str.replace('</a>', '') #strip all a tags
'''