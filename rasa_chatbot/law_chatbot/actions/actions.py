from random import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd


class QASRL_Pipeline:
    pass

# gives both questions and relevant answers for random law
class QASRLAction(Action):
    def name(self) -> Text:
        return "action_qasrl"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Load input sentences from CSV
        df = pd.read_csv('C:/Users/msi/Downloads/data.csv')
        input_sentences = df['sentences'].tolist()

        # Select a random input sentence (you can customize this logic)
        random_input = random.choice(input_sentences)

        # Instantiate QASRL pipeline
        qasrl_pipe = QASRL_Pipeline("kleinay/qanom-seq2seq-model-baseline")

        # Generate questions and answers
        qas_results = qasrl_pipe(random_input)

        # Extract relevant information from QAS results
        generated_text = qas_results[0]['generated_text']
        qas_pairs = qas_results[0]['QAs']

        # Construct a response
        response = f"Generated Text: {generated_text}\n"
        for qa_pair in qas_pairs:
            response += f"Question: {qa_pair['question']}\nAnswers: {', '.join(qa_pair['answers'])}\n"

        # Send the response to the user
        dispatcher.utter_message(text=response)

        return []
