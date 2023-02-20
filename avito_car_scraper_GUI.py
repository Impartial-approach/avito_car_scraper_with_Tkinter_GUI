import pandas as pd
import requests
from bs4 import BeautifulSoup
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

class AvitoScraper:

    def __init__(self, root):
        # Set up the root window
        root.title("Avito Auto Scraper")
        root.geometry("800x600")


        # Add a main frame to hold all the widgets
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add an inner frame to hold the city and page limit widgets
        inner_frame = tk.LabelFrame(main_frame, text="Settings", highlightbackground="white", highlightcolor="white")
        inner_frame.pack(pady=20, padx=10)

        # Create a dropdown menu for selecting search keywords
        default_keywords = ["voitures"]
        keyword_label = tk.Label(inner_frame, text="Type a keyword:")

        keyword_label.grid(row=0, column=0, padx=5, pady=5)
        keyword_var = tk.StringVar(value=default_keywords[0])  # Set default to "voitures"
        keyword_Entry = ttk.Entry(inner_frame, textvariable=keyword_var)
        keyword_Entry .grid(row=0, column=1, padx=5, pady=5)

        # Create a dropdown menu for selecting the city to scrape
        cities = ["Casablanca", "Rabat", "Marrakesh", "Fès", "Tanger", "Agadir", "Oujda", "Kenitra", "Tetouan",
                  "Mohammedia", "Tout le Maroc"]
        city_label = tk.Label(inner_frame, text="Select a city:")
        city_label.grid(row=1, column=0, padx=5, pady=5)
        city_var = tk.StringVar(value=cities[-1])  # Set default to "Tout le Maroc"
        city_dropdown = ttk.Combobox(inner_frame, textvariable=city_var, values=cities)
        city_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Create a dropdown menu for selecting the number of pages to scrape
        page_label = tk.Label(inner_frame, text="Page Limit:")
        page_label.grid(row=2, column=0, padx=5, pady=5)
        page_var = tk.IntVar(value=2)  # Set default to 2
        page_dropdown = ttk.Combobox(inner_frame, textvariable=page_var, values=list(range(2, 4000, 50)))
        page_dropdown.grid(row=2, column=1, padx=5, pady=5)

        # Add a button to start the scraping process
        start_button = tk.Button(main_frame, text="Scrape", font=('verdana', 8, 'bold'), bg="#FF0000", fg="white",
                                 width=50, height=2,
                                 command=lambda: self.scrape())
        start_button.pack(pady=20)

        # Add a label to show the status of the scraping process
        message_label = tk.Label(main_frame, text="", font=('verdana', 10))
        message_label.pack()

        # Add a button to save the scraped data to a file
        save_button = tk.Button(main_frame, text="Save to Excel", font=('verdana', 8, 'bold'), bg="#006400", fg="white",
                                width=15, height=2, command=self.save_to_excel, state=tk.DISABLED)
        save_button.pack(pady=20)

        # Save these widgets as instance variables so we can access them in other methods
        self.city_var = city_var
        self.page_var = page_var
        self.message_label = message_label
        self.save_button = save_button
        self.keyword_var = keyword_var





    def scrape(self):

        global df
        city = [self.city_var.get().lower() if self.city_var.get() != 'Tout le Maroc' else 'maroc'][0]
        page_limit=int(self.page_var.get())
        keywords= str(self.keyword_var.get()).lower()
        base_url = f'https://www.avito.ma/fr/{city}/{keywords}-%C3%A0_vendre'
        print(base_url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        data = []
        page_number = 1

        while True:
            if page_number < page_limit :
                url = base_url + '?o=' + str(page_number)
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()  # raise HTTPError for 4xx or 5xx response status codes
                    soup = BeautifulSoup(response.content, 'html.parser')
                except requests.exceptions.RequestException as e:
                    print(f"Error while getting response from {url}: {e}")
                    break

                listing_div = soup.find('div', {'class': 'sc-1nre5ec-0 dBrweF listing'})
                if not listing_div :
                    urls= None
                    # set the message label text
                    self.message_label.configure(text="No Matches Found ! ")
                    break
                else :
                    urls = [a['href'] for a in listing_div.find_all('a', href=True)]

                if not urls:
                    break

                for url in urls:

                    try:
                        response = requests.get(url, headers=headers)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.content, 'html.parser')
                    except requests.exceptions.RequestException as e:
                        print(f"Error while getting response from {url}: {e}")
                        continue  # skip current URL and proceed with next URL

                    if keywords ==  "voitures" :

                        details_div = soup.find('div', {'class': 'sc-1g3sn3w-4 eTmXXQ'})

                        items = details_div.find_all('li', {'class': 'sc-qmn92k-1 ldnQxr'})
                        price = ['' if not soup.find('p', {'class': 'sc-1x0vz2r-0 dYtyob sc-1g3sn3w-13 kliyMh'})
                                 else soup.find('p',
                                                {'class': 'sc-1x0vz2r-0 dYtyob sc-1g3sn3w-13 kliyMh'}).text.strip()][0]

                        # get the time and date of the ad
                        time_div = soup.find('div', {'class': 'sc-1g3sn3w-7 NuEic'})
                        print('----------------------------------------------------------')
                        time_element = time_div.find('time')
                        date_time = time_element['datetime']
                        date_time = datetime.strptime(date_time, '%m/%d/%Y, %I:%M:%S %p')

                        carburant_bvm_puissance = soup.find_all('span', {'class': 'sc-1x0vz2r-0 kuCwGF'})
                        for item in carburant_bvm_puissance:
                            if 'CV' in item.text.strip():
                                puissance = item.text.strip()
                            elif item.text.strip().lower() in ['manuelle', 'automatique']:
                                bvm_bva = item.text.strip()
                            else:
                                carburant = item.text.strip()

                        row = {}
                        for item in items:
                            label = item.find('span', {'class': 'sc-1x0vz2r-0 brylYP'}).text.strip()
                            value = item.find('span', {'class': 'sc-1x0vz2r-0 jsrimE'}).text.strip()
                            row['Ville'] = city

                            row[label] = value
                            row['Prix'] = price
                            row['Boite à Vitesse'] = bvm_bva
                            row['Puissance fiscale'] = puissance
                            row['Carburant'] = carburant
                            row["lien de l'annonce"] = url
                            row['date'] = datetime.date(date_time)
                            row['ad_life'] = datetime.today() - date_time

                            print(row)
                        data.append(row)

                    else :
                        #url = None
                        title_div= soup.find('div', {'class': 'sc-1g3sn3w-9 gIlAYt'})
                        title = ['' if not title_div else title_div.text][0]

                        details_div = soup.find('div', {'class': 'sc-1g3sn3w-4 eTmXXQ'})
                        description_div = soup.find('div', {'class': 'sc-1g3sn3w-16 leVIwi'})

                        description=['' if not description_div else description_div.text][0]

                        items = details_div.find_all('li', {'class': 'sc-qmn92k-1 ldnQxr'})
                        price = ['' if not soup.find('p', {'class': 'sc-1x0vz2r-0 dYtyob sc-1g3sn3w-13 kliyMh'})
                                 else soup.find('p',
                                                {'class': 'sc-1x0vz2r-0 dYtyob sc-1g3sn3w-13 kliyMh'}).text.strip()][0]

                        # get the time and date of the ad
                        time_div = soup.find('div', {'class': 'sc-1g3sn3w-7 NuEic'})
                        print('----------------------------------------------------------')
                        time_element = time_div.find('time')
                        date_time = time_element['datetime']
                        date_time = datetime.strptime(date_time, '%m/%d/%Y, %I:%M:%S %p')
                        row = {}
                        for item in items:
                            row['Title'] = title
                            row['Description'] = description
                            row['Prix'] = price
                            label = item.find('span', {'class': 'sc-1x0vz2r-0 brylYP'}).text.strip()
                            value = item.find('span', {'class': 'sc-1x0vz2r-0 jsrimE'}).text.strip()
                            row['Ville'] = city
                            row[label] = value
                            row['date'] = datetime.date(date_time)
                            row['ad_life'] = datetime.today() - date_time
                            row["lien de l'annonce"] = url


                        data.append(row)

                page_number += 1

            else:
                break


            df = pd.DataFrame(data)



            # set the message label text
            self.message_label.configure(text=f"Download completed , {len(df)} results were found . Click to Save to Excel")
            # open a save dialog box to get the file path and name
            self.save_button.config(state=NORMAL)

    def save_to_excel(self):

        # Get today's date and format it as a string
        date_str = datetime.now().strftime("%Y-%m-%d")
        export_path = f'avito_cars_for_sale_{date_str}.xlsx'
        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', initialfile=export_path)
        df.to_excel(file_path, index=False)



if __name__ == '__main__':
    root = tk.Tk()
    root.title("Avito Car Sales SCrapping Tool ")
    root.geometry('1000x500')
    my_gui = AvitoScraper(root)
    root.mainloop()





