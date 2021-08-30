import time
from datetime import datetime
import os
from bs4 import BeautifulSoup
#import twint
import pandas as pd
#from selenium import webdriver
import warnings
warnings.filterwarnings('ignore')
import streamlit as st
import re
from GrabzIt import GrabzItClient
from GrabzIt import GrabzItImageOptions
from GrabzIt import GrabzItTableOptions
#from webdriver_manager.chrome import ChromeDriverManager
from annotated_text import annotated_text
from urllib import request
from PIL import Image




class Scrap():
    def __init__(self):
        st.set_page_config(page_title='Data scraping from Web Site', layout= "wide")

        st.markdown(""" <style>
                    footer {visibility: hidden;}
                    </style> """, unsafe_allow_html=True)

        padding = 3
        st.markdown(f""" <style>
                    .reportview-container .main .block-container{{
                        padding-top: {padding}rem;
                        padding-right: {padding}rem;
                        padding-left: {padding}rem;
                        padding-bottom: {padding}rem;
                    }} </style> """, unsafe_allow_html=True)
        # button style
        st.markdown(" <style> .css-2trqyj:focus:not(:active) {border-color: #ffffff;box-shadow: none;color: #ffffff;background-color: #0066cc;}.css-2trqyj:focus:(:active) {border-color: #ffffff;box-shadow: none;color: #ffffff;background-color: #0066cc;}.css-2trqyj:focus:active){background-color: #0066cc;border-color: #ffffff;box-shadow: none;color: #ffffff;background-color: #0066cc;}</style> ", unsafe_allow_html=True)


    def run_app(self):
        self.frame()

    def frame(self):
        self.title()
        self.body()
        self.footer()

    def title(self):
        st.image("data/images/background.png", use_column_width=True)

    def footer(self):
        st.markdown('<i style="font-size:11px">alpha version 0.1</i>', unsafe_allow_html=True)

    def navigation(self, nav, name_product = None, link=None):
        st.session_state.nav = nav
        st.session_state.name_product = name_product
        st.session_state.link = link


    def time_nav(self, c_nav, t_nav):
        st.session_state.c_nav = c_nav
        st.session_state.t_nav = t_nav

    def body(self):
        if 'nav' not in st.session_state:
            st.session_state.nav = 'Home'

        if st.session_state.nav == 'Home':
            st.title('NFTs Overview')
            st.markdown("<h3>Discover the hottest NFT collections, marketplace rankings, and top real-time sales</h3>", unsafe_allow_html=True)

            self.image_scraping("https://dappradar.com/nft", 'top_15_collections', targetElement = '.sc-aKZfe', hideElement = '#om-nrz2xrzgki288pvo2jhx')
            self.image_scraping("https://dappradar.com/nft", 'top_5_sales', targetElement = '.sc-gIRixj', hideElement = '#om-nrz2xrzgki288pvo2jhx')
            self.image_scraping("https://dappradar.com/nft", 'top_5_marketplaces', targetElement = '.sc-kmASHI', hideElement = '#om-nrz2xrzgki288pvo2jhx')

            col1, col2, col3 = st.columns((1.5,0.2,1.1))
            with col1:
                st.markdown("<h1> Top 15 Collections </h1>", unsafe_allow_html=True)
                st.image("tables_of_collections/top_15_collections.png", use_column_width=True)
                st.button("Show All (More than 150)", key='Collections', on_click=self.navigation, args=('Collections', ))

            with col3:
                st.markdown("<h1> Top 5 Sales </h1>", unsafe_allow_html=True)
                st.image("tables_of_collections/top_5_sales.png", use_column_width=True)
                st.button("Show All", key='Sales', on_click=self.navigation, args=('Sales', ))

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<h1> Top 5 Marketplaces </h1>", unsafe_allow_html=True)
                st.image("tables_of_collections/top_5_marketplaces.png", use_column_width=True)
                st.button("Show All (Top 25)", key='Marketplaces', on_click=self.navigation, args=('Marketplaces', ))

        if st.session_state.nav == 'Collections':
            if 'c_nav' not in st.session_state:
                st.session_state.c_nav = 'table table-hover js-top-by-sales-table-24h summary-sales-table'
                st.session_state.t_nav = '24h'

            if 'link' not in st.session_state:
                st.session_state.link = ''

            st.title("Top Collections ")
            st.markdown("<h3>Rankings for NFT collections. Discover the top NFT collections across multiple protocols including Ethereum, BSC, WAX and Flow <br><br><br></h3>", unsafe_allow_html=True)

            #self.image_scraping("https://cryptoslam.io/", 'all_collections', targetElement = '.table')
            col1, col2, col3 = st.columns((1,1,5))
            col1.button('↩️ NFTs Overview', key='Home', on_click=self.navigation, args=('Home',))
            col2.button('💰 Marketplaces', key='Collections', on_click=self.navigation, args=('Marketplaces',))

            df = self.get_collections(st.session_state.c_nav,st.session_state.t_nav)
            st.markdown('<br><br>', unsafe_allow_html=True)
            st.markdown(annotated_text(("The Data was obtained at the time:", "", "#faa"), " ", str(datetime.now())), unsafe_allow_html=True)
            st.markdown('<br><br>', unsafe_allow_html=True)

            c0, c1, c2, c3, c4 = st.columns((6,1, 1, 1, 1))
            c1.button("24 hours", key='24 hours', on_click=self.time_nav, args=('table table-hover js-top-by-sales-table-24h summary-sales-table','24h',))
            c2.button("7 days", key='7 days', on_click=self.time_nav, args=('table table-hover js-top-by-sales-table-7d summary-sales-table', '7d',))
            c3.button("30 days", key='30 days', on_click=self.time_nav, args=('table table-hover js-top-by-sales-table-30d summary-sales-table', '30d',))
            c4.button("All time", key='All time', on_click=self.time_nav, args=('table table-hover js-top-by-sales-table-all summary-sales-table','all time',))

            st.markdown('-----')
            c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns((0.5, 0.3, 1, 1, 1, 0.9, 1, 1, 0.6))
            c1.markdown(annotated_text(('RANK', "", "#ffff"), "", ''), unsafe_allow_html=True)
            c3.markdown(annotated_text(('PRODUCT', "", "#ffff"), "", ''), unsafe_allow_html=True)
            c4.markdown(annotated_text(('SALES', "", "#ffff"), "", ''), unsafe_allow_html=True)
            if st.session_state.t_nav != 'all time':
                c5.markdown(annotated_text(('Change ('+st.session_state.t_nav+')', "", "#ffff"), "", ''), unsafe_allow_html=True)
            else:
                c5.markdown(annotated_text(('OWNERS', "", "#ffff"), "", ''), unsafe_allow_html=True)

            c6.markdown(annotated_text(('BUYERS', "", "#ffff"), "", ''), unsafe_allow_html=True)
            c7.markdown(annotated_text(('TRANSACTIONS', "", "#ffff"), "", ''), unsafe_allow_html=True)
            c8.markdown(annotated_text(('PROTOCOLE', "", "#ffff"), "", ''), unsafe_allow_html=True)
            c9.markdown(annotated_text(('ANALYSE', "", "#ffff"), "", ''), unsafe_allow_html=True)
            st.markdown('-----')

            for i in range(len(df)):
                RANK = df.loc[i, 'RANK']
                PRODUCT = df.loc[i, 'PRODUCT']
                SALES = df.loc[i, 'SALES']
                if st.session_state.t_nav != 'all time':
                    Change = df.loc[i, 'Change ('+st.session_state.t_nav+')']
                else:
                    OWNERS = df.loc[i, 'OWNERS']
                BUYERS = df.loc[i, 'BUYERS']
                TRANSACTIONS = df.loc[i, 'TRANSACTIONS']
                COLOR = df.loc[i, 'COLOR']
                PROTOCOLE = df.loc[i, 'PROTOCOLE']
                LINK = df.loc[i, 'LINK']

                c1,c2,c3,c4,c5,c6,c7,c8,c9 = st.columns((0.5,0.3,1,1,1,1,1,1,0.5))
                c1.markdown(annotated_text((RANK, "", "#ffff"), "",''), unsafe_allow_html=True)

                try:
                    c2.image("collections/"+PRODUCT+".png", use_column_width=True)
                except:
                    try:
                        img = Image.open("collections/" + PRODUCT + ".ico")
                        img.save("collections/" + PRODUCT + ".png", 'png')
                        c2.image("collections/" + PRODUCT + ".png", use_column_width=True)
                    except:
                        c2.image("collections/blank.png", use_column_width=True)

                c3.write(PRODUCT)
                c4.write(SALES)

                if COLOR == '#ca2d2d':
                    c5.write('🔻 ' + Change)
                elif COLOR== '#1d8843':
                    c5.write('🟩 ' + Change)
                else:
                    c5.write('🟡 ' + OWNERS)


                c6.write(BUYERS)
                c7.write(TRANSACTIONS)

                if PROTOCOLE == '/img/ethereum-logo.png':
                    c8.write('ETHEREUM')
                elif PROTOCOLE == '/img/ronin-logo.png':
                    c8.write('RONIN')
                elif PROTOCOLE == '/img/flow-logo.png':
                    c8.write('FLOW')
                elif PROTOCOLE == '/img/polygon-logo.png':
                    c8.write('POLYGON')
                elif PROTOCOLE == '/img/wax-logo.png':
                    c8.write('WAX')
                elif PROTOCOLE == '/img/bsc-logo.png':
                    c8.write('BSC')
                else:
                    c8.write('other')

                c9.button("🔍", key='Magnifying Glass '+str(i), on_click=self.navigation,
                          args=('Analyse',PRODUCT,LINK,))

                st.markdown('-----')



            # icon_list = df['ICONS'].tolist()
            # icon_name = df['PRODUCT'].tolist()
            # i = 0
            # path = re.sub("\\\web_scraping", "", os.path.abspath("collections"))
            # for url in icon_list:
            #     try:
            #         r = requests.get(url, allow_redirects=True)
            #
            #         if url[-3:] == 'ico':
            #             open(path +'\\'+icon_name[i]+'.ico', 'wb').write(r.content)
            #         else:
            #             open(path +'\\'+icon_name[i]+'.png', 'wb').write(r.content)
            #     except:
            #         print('error in '+str(i))
            #     i+=1

            st.write(df)




            # col1, col2, col3, col4 = st.columns((0.1,1,0.3,0.1))
            # col2.image("tables_of_collections/all_collections.png", use_column_width=True)
            # col3.image("tables_of_collections/protocols.png", use_column_width=True)


            # df = self.top_collections('https://dappradar.com/nft/collections')
            # st.write(df)


        if st.session_state.nav == 'Sales':
            st.title("Top Sales ")
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns((1,1,5))
            col1.button('↩️ NFTs Overview', key='Home', on_click=self.navigation, args=('Home',))
            col2.button('💎 Collections', key='Collections', on_click=self.navigation, args=('Collections',))


        if st.session_state.nav == 'Marketplaces':
            st.title("Top 25 Marketplaces (24h)")
            st.markdown("<h3>NFT marketplace rankings. Find non-fungible token trading volumes, number of traders per NFT marketplace and more key metrics. <br><br><br></h3>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns((1,1,5))
            col1.button('↩️ NFTs Overview', key='Home', on_click=self.navigation, args=('Home',))
            col2.button('💎 Collections', key='Collections', on_click=self.navigation, args=('Collections',))

            self.image_scraping("https://dappradar.com/nft/marketplaces/1", 'all_marketplaces', targetElement='.sc-iIEYCM',  hideElement='#om-nrz2xrzgki288pvo2jhx')

            col1, col2, col3 = st.columns((0.1, 1, 0.1))
            with col2:
                st.image("tables_of_collections/all_marketplaces.png", use_column_width=True)


        if st.session_state.nav == 'Analyse':
            c1, c2 = st.columns((0.7, 5))
            try:
                c1.image("collections/" + st.session_state.name_product + ".png", use_column_width=True)
            except:
                try:
                    img = Image.open("collections/" + st.session_state.name_product + ".ico")
                    img.save("collections/" + st.session_state.name_product + ".png", 'png')
                    c1.image("collections/" + st.session_state.name_product + ".png", use_column_width=True)
                except:
                    c1.image("collections/blank.png", use_column_width=True)

            c2.title(st.session_state.name_product + ' NFTs statistics')
            c2.markdown(st.session_state.name_product +' sales volume data, graphs & charts ', unsafe_allow_html=True)
            col1, col2, col3 = st.columns((1,1,5))
            col1.button('↩️ NFTs Overview', key='Home', on_click=self.navigation, args=('Home',))
            col2.button('💎 Collections', key='Collections', on_click=self.navigation, args=('Collections',))
            st.markdown('<br><br> ', unsafe_allow_html=True)


            link = 'https://cryptoslam.io'+st.session_state.link
            img = self.get_collections_seles(link, st.session_state.name_product)
            c1, c2, c3, c4 = st.columns(4)
            c1.caption('The USD value of sales from all marketplaces over the last 24 hour period')
            c2.caption('The number of owners making a purchase on any marketplace over the last 24 hour period')
            c3.caption('The number of owners selling a NFT on any marketplace over the last 24 hour period')
            c4.caption('The number of newly minted NFTs over the past 24 hour period')
            st.image(img, use_column_width=True)
            st.markdown('<br><br> ', unsafe_allow_html=True)

            path_file = self.get_summary_seles(link = 'https://cryptoslam.io'+st.session_state.link +'/sales/summary')
            if path_file is not None:
                df = pd.read_csv(path_file)
                df = df.iloc[:, 1:] # drop first column
                st.table(df)
                df = df.iloc[:-1] # drop last row
                st.markdown('<br><br> ', unsafe_allow_html=True)
                import altair as alt


                st.markdown('Total Transactions per Month', unsafe_allow_html=True)
                trans = alt.Chart(df).mark_line().encode(
                        x="Month",
                        y="Total Transactions:Q",
                        color = alt.value('#FFD700')
                    ).properties(width=500, height=400)
                st.altair_chart(trans, use_container_width=True)

                st.markdown('Sales (USD) per Month', unsafe_allow_html=True)
                df['Sales (USD)'] = df['Sales (USD)'].apply(lambda x: re.sub('\\$|,', '', x))
                sales = alt.Chart(df).mark_line().encode(
                    x="Month",
                    y="Sales (USD):Q",
                    color = alt.value('#FFD700')
                ).properties(width=500, height=400)
                st.altair_chart(sales, use_container_width=True)

                st.markdown('Sales (ETH) per Month', unsafe_allow_html=True)
                sales = alt.Chart(df).mark_line().encode(
                    x="Month",
                    y="Sales (ETH):Q",
                    color = alt.value('#FFD700')
                ).properties(width=500, height=400)
                st.altair_chart(sales, use_container_width=True)

                st.markdown('Avg Sale (USD) per Month', unsafe_allow_html=True)
                df['Avg Sale (USD)'] = df['Avg Sale (USD)'].apply(lambda x: re.sub('\\$','',x))
                Avg_usd = alt.Chart(df).mark_line().encode(
                    x="Month",
                    y="Avg Sale (USD):Q",
                    color = alt.value('#FFD700')
                ).properties(width=500, height=400)
                st.altair_chart(Avg_usd, use_container_width=True)

                st.markdown('Avg Sale (ETH) per Month', unsafe_allow_html=True)
                Avg_eth = alt.Chart(df).mark_line().encode(
                    x="Month",
                    y="Avg Sale (ETH):Q",
                    color = alt.value('#FFD700')
                ).properties(width=500, height=400)
                st.altair_chart(Avg_eth, use_container_width=True)
               
            else:
                st.markdown('<br><br><br>', unsafe_allow_html=True)
                st.markdown('No Data Found', unsafe_allow_html=True)
                st.markdown('<br><br><br>', unsafe_allow_html=True)

                


            # b = alt.Chart(df).mark_area(opacity=0.6).encode(
            #     x='Month', y='Total Transactions')
            # c = alt.layer(a, b)

















    def parsing_data(self, text):
        return re.sub("(\xa0)|(\n)|(\r)|(\")|(\'),", "",text)


    def image_scraping(self, URLToImage, FileName, targetElement = None, hideElement = None):
        if targetElement is not None or hideElement is not None:
            options = GrabzItImageOptions.GrabzItImageOptions()
        if targetElement is not None:
            options.targetElement = targetElement
        if hideElement is not None:
            options.hideElement = hideElement

        grabzIt = GrabzItClient.GrabzItClient("MWRiMTVhYTcwM2Y5NDIzODlhNmUwYzdlNmUwYzMyYjY=", "Fj9ePz8/Pz8/Pwk/HT8/cS9ZP1FxYg8/Pz8aGT8fJj8=")
        try:
            grabzIt.URLToImage(URLToImage, options)
        except:
            grabzIt.URLToImage(URLToImage)

        #path = re.sub("\\\web_scraping", "", os.path.abspath("tables_of_collections"))
        path = '/home/ubuntu/Ziyad_Apps/nfts_data_scraping/tables_of_collections/'
        grabzIt.SaveTo(path +FileName+".png")



    def driver_config(self, executable_path):
        global driver
        option = webdriver.ChromeOptions()
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('--incognito')
        option.add_argument('--headless')
        driver = None
        try:
            driver = webdriver.Chrome(
                executable_path = executable_path,
                options = option)
        except:
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)

        return driver

    def git_page_source(self, url):
        driver = self.driver_config("C:/Users/hp/.wdm/drivers/chromedriver/win32/91.0.4472.101/chromedriver.exe")
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        #driver.close()
        return soup

    def top_collections(self, url):
        soup = self.git_page_source(url)
        gdp = soup.find_all("div", attrs={"class": "sc-kmASHI sc-cvJHqN eeGfwZ cktZhQ rankings-table"})
        try:
            body = gdp.find_all("div", recursive=False)
        except:
            body = gdp[0].find_all("div", recursive=False)

        head = body[2]
        body_rows = body[3:]

        headings = []
        h = head.find("div").find("div")
        for item in h.findChildren("div"):
            item = (item.text).rstrip("\n")
            headings.append(item)
        #print(headings)

        all_rows = []
        for row_num in range(len(body_rows)):
            row = []

            row_item = body_rows[row_num].findChildren("div", recursive=False)

            rank = row_item[0]
            row.append(self.parsing_data(rank.text))

            Children = row_item[1].findChildren("div", recursive=False)

            name = Children[1].find("a", attrs={'class': 'nft-name-link'})
            if name is None:
                name = Children[1].find("span", attrs={'class': 'nft-name-link'})
            row.append(self.parsing_data(name.text))

            # try:
            #     src = Children[0].find('img')['src']
            # except:
            #     src = name.text
            # row.append(src)

            crypto = Children[1].find("div", attrs={'class': 'sc-jHVexB epRmzg'})
            row.append(self.parsing_data(crypto.text))

            Volume = row_item[2].findChildren("div", recursive=False)
            row.append(self.parsing_data(Volume[0].text))
            row.append(self.parsing_data(Volume[1].text))

            Traders = row_item[3].findChildren("div", recursive=False)
            row.append(self.parsing_data(Traders[0].text))
            row.append(self.parsing_data(Traders[1].text))

            Sales = row_item[4].findChildren("div", recursive=False)
            row.append(self.parsing_data(Sales[0].text))
            row.append(self.parsing_data(Sales[1].text))

            all_rows.append(row)

        #print(all_rows)

        headings.insert(0, 'RANK')
        #headings.insert(2, 'ICONE')
        headings.insert(3, 'PROTOCOLS')
        headings.insert(5, 'VOLUME CHANGE')
        headings.insert(7, 'TRADERS CHANGE')
        headings.insert(9, 'SALES CHANGE')

        df = pd.DataFrame(data=all_rows, columns=headings)
        return df
        # df.to_csv(r'result.csv', index=False)
        # print(df)

    def get_collections(self, class_name, time):
        response = request.urlopen("https://cryptoslam.io/")
        page_source = response.read()
        soup = BeautifulSoup(page_source, 'html.parser')
        gdp = soup.find_all("table", attrs={"class": class_name})
        table1 = gdp[0]
        body = table1.find_all("tr")
        head = body[0]
        body_rows = body[1:]

        all_rows = []

        for row_num in range(len(body_rows)):
            row = []
            for row_item in body_rows[row_num].find_all("td"):

                aa = re.sub("(\xa0)|(\n)|(\r)|,", "", row_item.text)
                try:
                    row_item = row_item.find("span", attrs={'class': re.compile("product-name")})
                    aa = re.sub("(\xa0)|(\n)|(\r)|,", "", row_item.text)
                except:
                    pass

                row.append(aa)

            for row_item in body_rows[row_num].find_all("td"):  # loop through all row entries
                try:
                    img = row_item.img['src']
                    row.append(img)
                except:
                    pass

            try:
                color = body_rows[row_num].find('td', attrs={'class': 'summary-sales-table__column summary-sales-table__column-change '
                                                            'summary-sales-table__no-wrap cursor-default'}).find('span')
                color = color['style'][7:14]
                row.append(color)
            except:
                row.append("no color")

            try:
                product_link = body_rows[row_num].find("td", attrs={'class': 'summary-sales-table__column summary-sales-table__column-product summary-sales-table__cell-product product'})
                product_link = product_link.find('a')
                product_link = product_link['href']
                row.append(product_link)
            except:
                row.append("no link")

            all_rows.append(row)


        headings = ['RANK','PRODUCT','None','SALES','Change ('+time+')','BUYERS','TRANSACTIONS','ICONS','PROTOCOLE','COLOR', 'LINK']
        if time == 'all time':
            headings = ['RANK', 'PRODUCT', 'None', 'SALES', 'BUYERS', 'TRANSACTIONS', 'OWNERS', 'ICONS', 'PROTOCOLE', 'COLOR', 'LINK']

        df = pd.DataFrame(data=all_rows, columns=headings)
        del df['None']

        return df
        # df.to_csv(r'hjhugy.csv', index=False)
        # print(df)


    def get_collections_seles(self, link, filename):
        options = GrabzItImageOptions.GrabzItImageOptions()
        # options.targetElement = 'div.statistics-row__stat:nth-child(1) div:nth-child(1) div:nth-child(2) a:nth-child(1) div:nth-child(2) div:nth-child(2)'
        options.waitForElement = 'div.statistics-row__stat:nth-child(1) div:nth-child(1) div:nth-child(2) a:nth-child(1) div:nth-child(2) div:nth-child(2) canvas:nth-child(1)'
        options.targetElement = 'div.statistics-row'
        options.hideElement = 'div.ibox-content:nth-child(5) , .fa, .fab, .fal, .far, .fas'
        options.delay=1000
        grabzIt = GrabzItClient.GrabzItClient("MWRiMTVhYTcwM2Y5NDIzODlhNmUwYzdlNmUwYzMyYjY=","Fj9ePz8/Pz8/Pwk/HT8/cS9ZP1FxYg8/Pz8aGT8fJj8=")
        grabzIt.URLToImage(link, options)
        #path = re.sub("\\\web_scraping", "", os.path.abspath("tables_of_collections"))
        #grabzIt.SaveTo(path + "\\" + filename + ".png")
        path = '/home/ubuntu/Ziyad_Apps/nfts_data_scraping/tables_of_collections/'
        grabzIt.SaveTo(path +filename+".png")
        return path +filename+".png"

    def get_summary_seles(self, link):
        grabzIt = GrabzItClient.GrabzItClient("MWRiMTVhYTcwM2Y5NDIzODlhNmUwYzdlNmUwYzMyYjY=",
                                              "Fj9ePz8/Pz8/Pwk/HT8/cS9ZP1FxYg8/Pz8aGT8fJj8=")
        options = GrabzItTableOptions.GrabzItTableOptions()
        options.tableNumberToInclude = 1
        grabzIt.URLToTable(link, options)
        # Then call the Save or SaveTo method
        #path = re.sub("\\\web_scraping", "", os.path.abspath("tables_of_collections"))
        #grabzIt.SaveTo(path + "\\" + "summary.csv")
        path = '/home/ubuntu/Ziyad_Apps/nfts_data_scraping/tables_of_collections/'
        try :
            grabzIt.SaveTo(path +"summary.csv.png")
            return path +"summary.csv.png"
        except:
            return None






#
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')
# #driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
# driver = webdriver.Chrome(executable_path="C:/Users/hp/.wdm/drivers/chromedriver/win32/91.0.4472.101/chromedriver.exe",options=options)
# url = "https://dappradar.com/nft/collections"
# driver.get(url)
#
#
#
# content = driver.page_source
# soup = BeautifulSoup(content, features="html.parser")
# driver.close()
#
# gdp = soup.find_all("div", attrs={"class": "sc-kmASHI sc-cvJHqN eeGfwZ cktZhQ rankings-table"})
# try :
#     body = gdp.find_all("div", recursive=False)
# except:
#     body = gdp[0].find_all("div", recursive=False)
#
# head = body[2]
# body_rows = body[3:]
#
# headings = []
# h = head.find("div").find("div")
# for item in h.findChildren("div"):
#     item = (item.text).rstrip("\n")
#     headings.append(item)
# print(headings)
#
#
# all_rows = []
# for row_num in range(len(body_rows)):
#     row = []
#
#     row_item = body_rows[row_num].findChildren("div", recursive=False)
#
#     rank = row_item[0]
#     row.append(parsing_data(rank.text))
#
#     Children = row_item[1].findChildren("div", recursive=False)
#
#     name = Children[1].find("a", attrs={'class': 'nft-name-link'})
#     if name is None:
#         name = Children[1].find("span", attrs={'class': 'nft-name-link'})
#     row.append(parsing_data(name.text))
#     try :
#         src = Children[0].find('img')['src']
#     except:
#         src = name.text
#     row.append(src)
#
#     crypto = Children[1].find("div", attrs={'class': 'sc-jHVexB epRmzg'})
#     row.append(parsing_data(crypto.text))
#
#     Volume = row_item[2].findChildren("div", recursive=False)
#     row.append(parsing_data(Volume[0].text))
#     row.append(parsing_data(Volume[1].text))
#
#     Traders = row_item[3].findChildren("div", recursive=False)
#     row.append(parsing_data(Traders[0].text))
#     row.append(parsing_data(Traders[1].text))
#
#     Sales = row_item[4].findChildren("div", recursive=False)
#     row.append(parsing_data(Sales[0].text))
#     row.append(parsing_data(Sales[1].text))
#
#     all_rows.append(row)
#
# print(all_rows)
#
# headings.insert(0,'rank')
# headings.insert(2,'icone')
# headings.insert(3,'crypto-chaine')
# headings.insert(5,'volume-change')
# headings.insert(7,'traders-change')
# headings.insert(9,'sales-change')
#
# df = pd.DataFrame(data=all_rows, columns=headings)
# df.to_csv(r'result.csv', index = False)
# print(df)

#------------------------------------------
#------------------------------------------
#------------------------------------------









# #------------------------- test
# all_rows = []
# for row_num in range(len(body_rows)):
#     row = []
#     for row_item in body_rows[row_num].findChildren("div", recursive=False):
#         children = row_item.findChildren("div", recursive=False)
#         if len(children)==0:
#             row.append(row_item.text)
#         else:
#             for row_item_2 in children:
#                 name = row_item_2.find("a", attrs={'class': 'nft-name-link'})
#                 crypto = row_item_2.find("div", attrs={'class': 'sc-jHVexB epRmzg'})
#                 prjt_img = row_item_2.find("img", attrs={'class': 'sc-dwfUOf bNQBLt img-loaded'})
#                 if name is not None and crypto is not None:
#                     row.append(name.text)
#                     row.append(crypto.text)
#                 elif prjt_img is not None:
#                     row.append(prjt_img['src'])
#                 else:
#                     row.append(row_item_2.text)
#
#     all_rows.append(row)
# #print(all_rows)
# headings.insert(0,'rank')
# headings.insert(1,'icone')
# headings.insert(3,'crypto-chaine')
# headings.insert(5,'volume-change')
# headings.insert(7,'traders-change')
# headings.insert(9,'sales-change')
#
# df = pd.DataFrame(data=all_rows, columns=headings)
# df.to_csv(r'result.csv', index = False)
# print(df.head(10))





















# def display_profile(username):
#     def get_collection(username):
#         c = twint.Config()
#         c.Username = username
#         c.Hide_output = True
#         twint.run.Lookup(c)
#         collection = twint.output.users_list[-1]
#         return collection
#
#     try:
#         # get the profile_pic_url
#         collection = get_collection(username)
#         prof_pic = collection.avatar.replace("normal", "100x100")
#         # download the image in a folder called static I created
#         response = requests.get(prof_pic)
#         filename = "collections/username.jpg"
#         with open(filename, "wb") as f:
#             f.write(response.content)
#
#         return filename
#     except:
#         return None
