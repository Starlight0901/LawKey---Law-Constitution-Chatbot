# Training
    rasa train --force 

# Testing
    Rasa NLU test -> rasa test nlu --nlu data/nlu.yml --model models
    Rasa core test -> rasa test core --stories stories.yml --out results

# To run the bot (**Terminal**)
    Local1 -> rasa run actions  
    Local2 -> rasa shell 

# Actions 
    retrieve_laws ( It preprocesses input using TF-IDF and Word2Vec for vectorization, calculating cosine similarity to find relevant laws. If similarity exceeds a threshold, it retrieves and presents the top relevant laws and summaries.)
    handle_complaint_details (Records user complaints into a CSV file.)

# Configurations

    1. CountVectorsFeaturizer: This is a featurization component used for converting text data into numerical feature vectors. It's commonly used in text classification tasks and is a part of the NLU pipeline.
    2. DIETClassifier: This is a neural network-based model used for intent classification and entity extraction. It's trained on labeled examples of user messages and their corresponding intents and entities.
    3. TEDPolicy: This is a policy model based on the Transformer Embedding Dialogue model. It's used for dialogue management, predicting the next action based on the current state of the conversation.
    4. EntitySynonymMapper: This component maps synonymous entity values to a common canonical form. It's used to improve the consistency of entity recognition.
    5. ResponseSelector: This component is used for response selection when a user message matches a predefined retrieval intent. It's trained to select appropriate responses from a predefined set of responses.
    6. MemoizationPolicy: This policy memorizes previous conversation paths and actions to predict the next action based on the current state. It's used for dialogue management based on past conversation history.
    7. RulePolicy: This policy uses rules to handle specific conversation paths. It's used to define fixed response paths for certain intents or conditions.
    8. 'TEDPolicy': This policy uses the Transformer Embedding Dialogue model for dialogue management. It's being trained over 100 epochs.

These components and policies use machine learning techniques to **process user messages, classify intents, extract entities, manage dialogue, and select responses, enabling this chatbot to understand user inputs and respond accordingly**.

