import pytest
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from actions.actions import RetrieveLaws


@pytest.fixture
def tracker():
    sender_id = "test"
    slots = {}
    latest_message = {}
    events = []
    paused = False
    followup_action = None
    active_loop = {}
    latest_action_name = None  # Add this line to include the missing argument

    return Tracker(sender_id, slots, latest_message, events, paused, followup_action, active_loop, latest_action_name)


def test_retrieve_laws_action(tracker):
    action = RetrieveLaws()
    dispatcher = CollectingDispatcher()
    domain = {}

    # Set up a mock user input
    user_input = ("Which court should an individual apply to for maintenance if they, the person in respect of whom "
                  "the application is made, or the person against whom the application is made resides within its "
                  "jurisdiction?")

    tracker.latest_message = {"text": user_input}

    # Run the action
    action.run(dispatcher, tracker, domain)

    # Retrieve the response from the dispatcher
    response = dispatcher.messages[0]['text']

    # Assert that the response contains the expected message
    assert ("An application for maintenance may be made to the Magistrates Court within whose jurisdiction the "
            "applicant or the person in respect of whom the application is made or the person against whom such "
            "application is made, resides.") in response

# this test case simulates the execution of the RetrieveLaws action in a Rasa chatbot environment and verifies that
# the action produces the expected response given a specific input message
