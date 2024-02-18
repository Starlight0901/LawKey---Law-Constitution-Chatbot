# test_integration.py

import requests
import pytest


@pytest.mark.parametrize("user_input, expected_response", [
    ("What are the relevant laws?", "Here are the top 3 relevant laws based on your query:"),
    ("What happens to an allowance for the maintenance of a child, adult offspring, or disabled offspring under this Act once the individual in question no longer falls within the defined categories?","No Order for an allowance for the maintenance of any child, adult offspring or disabled offspring made under this Act shall, except for the purpose of recovering money previously due under such order, be of any force or validity after the person in respect of whom the order is made ceases to be a child, adult offspring or disabled offspring, as the case may be, within the meaning of this Act."),
    ("What are the requirements regarding the form and stamp duty for applications for maintenance orders or to enforce such orders, as well as for summonses to respondents or witnesses?", "Every application for an order of maintenance or to enforce such an order, shall be in writing and shall be signed by the applicant or the person making the application on his behalf and shall be free of any stamp duty. Every summons to a respondent or a witness shall also be free of stamp duty. "),
    ("Which court should an individual apply to for maintenance if they, the person in respect of whom the application is made, or the person against whom the application is made resides within its jurisdiction?", " An application for maintenance may be made to the Magistrates Court within whose jurisdiction the applicant or the person in respect of whom the application is made or the person against whom such application is made, resides."),
    ("Which forms are designated for specific purposes as outlined in the Schedule to Maintenance Act, and under what conditions may variations to these forms be applied?","The forms specified in the Schedule to this Act, with such variations as the circumstances of any case may require, shall be used for the respective purposes therein mentioned. "),
    ("In cases of discrepancy between the Sinhala and Tamil versions of Maintenance Act, which text takes precedence according to the specified provision?","In the event of any inconsistency between the Sinhala and Tamil texts of this Act, the Sinhala text shall prevail "),
    ("Does any provision within this Act imply a deprivation of the right for an individual, such as a child, adult offspring, disabled offspring, spouse, or parent, to pursue a civil action for maintenance?","in Maintenance Act shall be construed as depriving a person including a child, adult offspring, disabled offspring, spouse or parent of the right, if any to maintain a civil action for maintenance."),
    ("Which sections of the Married Women Property Ordinance are affected by the amendment stated within Maintenance Act?","The Married Women Property Ordinance is hereby amended by the repeal of section 26 and section 27 of that Ordinance.")
    # Add more test cases as needed
])
def test_retrieve_laws_action(user_input, expected_response):
    response = requests.post("http://localhost:5005/webhooks/rest/webhook", json={"message": user_input})
    assert response.status_code == 200
    responses = response.json()
    assert any(expected_response in r['text'] for r in responses)
