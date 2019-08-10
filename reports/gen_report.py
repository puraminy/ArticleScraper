import pandas as pd
import io


def genHtml(df, html_fname, total=-1, search_terms='none', from_year='all'):
    css_file = 'df_style.css'
    # df.reset_index()
    pub_name = df['pub_name'].iloc[0]
    pub_url = df['pub_url'].iloc[0]
    html_string = '''
    <html>
      <head><title>HTML Pandas Dataframe with CSS</title></head>
      <link rel="stylesheet" type="text/css" href="''' + css_file + '''"/>
      <body>
        {div}
      </body>
    </html>.
    '''
    # div = df.to_html(classes=class_name)
    sel = len(df)
    total = sel if total < 0 else total
    div = f'''
    <div>
    <div>
        <span>Conference</span><span><a href="{pub_url}">{pub_name}</a></span>
    </div>
    <div>
        <span>Search terms</span><span>{search_terms}</span>
    </div>
    <div>
        <span>Percentage</span><span>{sel} of {total} = {round(sel/total,2)*100}%</span>
    </div>
    <div>
        <div >From</div><div>{from_year}</div>
    </div>
    </div>
    <div border="1" class="dataframe mystyle">
    <div>
    <div colspan=3>Papers</div>
    </div>
    '''
    for index, row in df.iterrows():
        year = row['issue_year']
        title = row['paper_title']
        url = row['paper_url']
        abstract = row['paper_abstract']
        s = f'<div class="paper_item">'
        s += f'<h3 class="paper_title"><span class="paper_index">{index}:</span><a href="{url}">{title}</a><span class="paper_year">({year})</span></h3>'
        s += f'<p class="paper_abstract">{abstract}</p></div>'
        div += s
    div += '</div>'
    # OUTPUT AN HTML FILE
    with io.open(html_fname, "w", encoding="utf-8") as f:
        f.write(html_string.format(div=div))



df = pd.read_csv('../data/aclweb.csv')
pd.set_option('colheader_justify', 'center')   # FOR div <th>
total = len(df)
search_terms = 'knowledge'
sel_df = df.loc[df['paper_abstract'].notnull()]
print(len(sel_df))
genHtml(sel_df[:50], 'report3.html', total, search_terms=search_terms)

