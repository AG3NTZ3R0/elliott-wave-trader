import os
import time

import argparse
import pandas as pd

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from rich.console import Console
from rich.table import Table

class ElliottWaveTrader:
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='A CLI tool to perform data transformations on Elliott Wave Trade Wave Setups.')
        self.parser.add_argument('--symbol', type=str, help='Ticker symbol')
        self.parser.add_argument('--sort', nargs='+', help='Columns to sort by')
        self.parser.add_argument('--ascending', nargs='+', help='True/False for each sort column', 
            type=lambda x: x.lower() == 'true'
        )
        
        self.args = self.parser.parse_args()

        self.classification_columns = ['Type', 'Time', 'Rank']
        self.date_columns = ['Initial Date', 'Update Date']
        self.numerical_columns = ['Support', 'Invalidation', 'Resistance', 'Target', 'Latest']

    def _display(self, df):
        table = Table(title="Wave Setups")

        for column in df.columns:
            if column in self.classification_columns:
                table.add_column(column, style="cyan", justify='center')
            elif column in self.date_columns:
                table.add_column(column, style="cyan", justify='center')
            elif column in self.numerical_columns:
                table.add_column(column, style="cyan", justify='right')
            else:
                table.add_column(column, style="cyan")
        
        for row in df.itertuples(index=False):
            table.add_row(*[str(value) for value in row])

        console = Console()
        console.print(table, justify='center')

    def _ingest(self):
        options = Options()
        options.add_argument('--headless')  # Optional: Run in headless mode if you don't need to see the browser
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            login_url = 'https://www.elliottwavetrader.net/login'
            driver.get(login_url)

            email_field = driver.find_element(By.NAME, 'email')
            password_field = driver.find_element(By.NAME, 'password')
            submit_button = driver.find_element(By.NAME, 'submit')

            email_field.send_keys(os.environ.get('ELLIOTT_WAVE_TRADER_USERNAME'))
            password_field.send_keys(os.environ.get('ELLIOTT_WAVE_TRADER_PASSWORD'))
            submit_button.click()

            protected_url = 'https://www.elliottwavetrader.net/stockwaves/wave-setups'
            driver.get(protected_url)

            if self.args.symbol is not None:
                ticker_field = driver.find_element(By.NAME, 'ticker')
                search_button = driver.find_element(By.ID, 'search-submit')

                ticker_field.send_keys(self.args.symbol)
                search_button.click()

            table = driver.find_element(By.CLASS_NAME, 'table')
            headers = [header.text for header in table.find_element(By.TAG_NAME, 'thead').find_element(By.TAG_NAME, 'tr').find_elements(By.TAG_NAME, 'th')]
            rows = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            data = [[cell.text for cell in row.find_elements(By.TAG_NAME, 'td')] for row in rows]

            return pd.DataFrame(data, columns=headers)

        finally:
            driver.quit()

    def _transform(self, df):
        df = df.rename(columns={'Ranking': 'Rank', 'Latest Price': 'Latest', 'Initial Set-up': 'Initial Date'})

        df['Type'] = df['Type'].replace({'Long': 'L', 'Short': 'S'})

        df[self.numerical_columns] = df[self.numerical_columns].apply(pd.to_numeric)
        df['% Progress'] = ((df['Latest'] - df['Support']) / (df['Target'] - df['Support']) * 100).round(2)
        self.numerical_columns.append('% Progress')
        # TODO: Add % Potential. The formula is different depending upon whether the setup is short or long type.
        # self.numerical_columns.append('% Potential')

        if self.args.sort is not None:
            if self.args.ascending is not None:
                df = df.sort_values(self.args.sort, ascending=self.args.ascending)
            else:
                df = df.sort_values(self.args.sort)
        
        df[self.date_columns] = df[self.date_columns].apply(pd.to_datetime, format='%d-%b-%y')
        df[self.date_columns] = df[self.date_columns].apply(lambda x: x.dt.strftime('%d-%m-%y'))
        df[self.numerical_columns] = df[self.numerical_columns].apply(lambda x: [f'{float(val):.2f}' for val in x])

        df.insert(2, 'Time', df.pop('Time'))
        df.insert(3, 'Rank', df.pop('Rank'))
        df.insert(10, '% Progress', df.pop('% Progress'))
        # Insert % Potential

        df.pop('Industry')
        df.pop('Last Video')

        return df

    def execute(self):
        df = self._ingest()    
        df = self._transform(df)

        self._display(df)

