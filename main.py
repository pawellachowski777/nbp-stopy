import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib3
urllib3.disable_warnings()


def download_data(soup):
    html_data = soup.find_all('tr', {'valign': 'middle'})

    rows = []
    for tr in html_data:
        td = tr.find_all('td')
        row = [tr.text.replace(" ", "").replace(",", ".") for tr in td]

        # wyrzucenie pustych wierszy i wierszy z samym rokiem
        try:
            int(row[0])
        except (IndexError, TypeError, ValueError):
            if row:
                rows.append(row)

    nbp_df = pd.DataFrame(rows,
                          columns=['obowiązuje_od', 'stopa_referencyjna', 'stopa_lombartowa', 'stopa_depozytowa',
                                   'stopa_redyskontowa_weksli', 'stopa_dyskontowa_weksli'])
    nbp_df.replace("*", None, inplace=True)

    # stringi na liczby i datę
    nbp_df.iloc[:, 1:] = nbp_df.iloc[:, 1:].astype(float)
    nbp_df['obowiązuje_od'] = pd.to_datetime(nbp_df['obowiązuje_od'])
    nbp_df['obowiązuje_od'] = nbp_df['obowiązuje_od'].dt.date

    return nbp_df


path = r"https://www.nbp.pl/home.aspx?f=/dzienne/stopy_archiwum.htm"
page = requests.get(path, verify=False)
soup = BeautifulSoup(page.content, 'html.parser')

nbp_df = download_data(soup)

nbp_df.to_excel('stopy_nbp.xlsx', index=False)
