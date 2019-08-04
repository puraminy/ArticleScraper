import pandas as pd
import io


def genHtml(df, html_fname, total=-1, search_terms='none', from_year='all'):
    css_file = 'df_style.css'
    conf_name = df.loc[0, 'conf_name']
    conf_url = df.loc[0, 'conf_url']
    html_string = '''
    <html>
      <head><title>HTML Pandas Dataframe with CSS</title></head>
      <link rel="stylesheet" type="text/css" href="''' + css_file + '''"/>
      <body>
        {table}
      </body>
    </html>.
    '''
    # table = df.to_html(classes=class_name)
    sel = len(df)
    total = sel if total < 0 else total
    table = f'''
    <table border="1" class="dataframe mystyle">
    <tr>
        <td colspan=2>Conference</td><td><a href="{conf_url}">{conf_name}</a></td>
    </tr>
    <tr>
        <td colspan=2>Search terms</td><td>{search_terms}</td>
    </tr>
    <tr>
        <td colspan=2>Percentage</td><td>{sel} of {total} = {round(sel/total,2)*100}%</td>
    </tr>
    <tr>
        <td colspan=2>From</td><td>{from_year}</td>
    </tr>
    <tr>
    <td colspan=3>Papers</td>
    </tr>
    '''
    for index, row in df.iterrows():
        year = row['proc_year']
        title = row['paper_title']
        url = row['paper_url']
        abstract = row['paper_abstract']
        s = f'<tr><td>{index}</td>'
        s += f'<td>{year}</td><td><a href="{url}">{title}</a></td>'
        s += f'</tr><tr><td colspan=3><p>{abstract}</p></td></tr>'
        table += s
    table += '</table>'
    # OUTPUT AN HTML FILE
    with io.open(html_fname, "w", encoding="utf-8") as f:
        f.write(html_string.format(table=table))



df = pd.read_csv('../data/db.csv')
pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
total = len(df)
sel_df = df.loc[df['proc_year'] > 2014]
genHtml(sel_df, 'report3.html', total)

