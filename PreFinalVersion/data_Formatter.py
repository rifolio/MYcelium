from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

"""
This class handles the schema matching and formatting of data
"""


class DataFormatter:

    @staticmethod
    def match_schema(source_csv, destination_csv):
        prompt = (f"I have the following two sqlite files:\nSource:\n{source_csv}\n\nDestination:\n{destination_csv}\n"
                  f"\nI want you to format the source file to match the schema of the destination file.\n\nThe idea "
                  f"is that the first file is joining the second file and so therefore it needs to fit its structure "
                  f"and format.\nYou need to look at the columns of both files and make sure that the data inside the "
                  f"source column fits the data inside the destination columns.\n\nFor example\nData1: \nLastname, "
                  f"Sex, Name\nSmith, M, John\n\nData2: \nName, LastName, Gender\nJane, Doe, Female\n\nAfter schema "
                  f"matching: \nName, LastName, Gender\nJohn, Smith, Male\nJane, Doe, Female\n\nOnly show the "
                  f"formatted data and nothing else.")
        client = OpenAI(api_key="KEYHERE")
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0,
            max_tokens=300
        )

        formatted_data = response.choices[0].text.strip()
        return formatted_data
