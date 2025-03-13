import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ai import CustomAI
from sqlalchemy import create_engine, Table, MetaData, insert, update


def create_driver():
    """customizing selenium webdriver
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_company_sitemap_urls(df):
    companies_data = []
    for url in df["Website Url"]:
        print(url)
        company_name = df[df["Website Url"] == url]["Company Name"].values[0]
        print(company_name)
        page_links = []
        site_resp = requests.get(url.strip())
        if site_resp.status_code == 200:
            driver = create_driver()
            try:
                driver.get(url)
                time.sleep(10)

                link_tags = driver.find_elements(By.TAG_NAME, "a")
                for tag in link_tags:
                    link = tag.get_attribute("href")
                    if link and "http" in link:
                        # print(link)
                        page_links.append(link)
            except:
                pass
            driver.quit()

        ai_assist = CustomAI()
        prompt = """
        "You are analyzing a company's online presence based on its sitemap. 
        Read the content containing all the site links carefully.
        Based on these links and their structure, generate a concise business insight about the 
        company. Identify key focus areas, business priorities, and any 
        indications of growth, investment, or technology adoption. 
        Format the response as:
        "- Company Overview: This company does this.
        - Key Focus Areas: Their focus areas are x,y,z.
        - Potential Opportunities: They need help in a,b,c products or We can help in a,b,c."
        """
        ai_resp = ai_assist.openai_check_content(prompt=prompt, content=f"{page_links}")
        companies_data.append({"company_name":company_name, "company_url":url, "page_links":f"{page_links}", "ai_resp":ai_resp})
    return companies_data


# if __name__ == "__main__":
def main(df, openai_api_key, output_file_path, db_user, db_password, db_host, db_port, db_name):

    # load_dotenv(override=True)
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = openai_api_key

    if not openai_api_key:
        raise Exception("please configure openai api key in environment")

    # df = pd.read_excel("input_companies.xlsx", engine="openpyxl")
    companies_data = get_company_sitemap_urls(df)
    df_output = pd.DataFrame(companies_data)
    # df_output.to_csv("output.csv", index=False)
    df_output.to_csv(f"{output_file_path}/processed_file.csv", index=False)

    connection_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_url)
    # df_output.to_sql("SQL_test_data", engine, if_exists='replace', index=False)

    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables['scraper_data']

    # Add or update rows
    with engine.begin() as connection:
        for index, row in df_output.iterrows():
            query = connection.execute(table.select().where(table.c.company_url == row['company_url']))
            if query.rowcount > 0:  # Company URL exists, update the row
                connection.execute(
                    table.update().where(table.c.company_url == row['company_url']).values(
                        company_name=row['company_name'],
                        company_url=row['company_url'],
                        page_links=row['page_links'],
                        ai_resp=row['ai_resp']
                    )
                )
            else:  # Company URL doesn't exist, insert as new row
                connection.execute(
                    table.insert().values(
                        company_name=row['company_name'],
                        company_url=row['company_url'],
                        page_links=row['page_links'],
                        ai_resp=row['ai_resp']
                    )
                )

    return df_output
