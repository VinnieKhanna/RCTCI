import pandas as pd

df = pd.read_csv('./problem_data.csv')

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
df.to_csv('./cleaned_desc.csv')