If you want to compute similarity between user input and your dataset using a Word2Vec model, you would need to load the Word2Vec model separately in your action code. Here's what it means in more detail:

1. **Loading the Word2Vec Model**: Word2Vec is a popular word embedding technique that represents words as dense vectors in a continuous vector space. These vectors capture semantic meanings of words based on the contexts they appear in. To compute similarity between user input and your dataset using Word2Vec, you first need to load a pre-trained Word2Vec model or train your own.

2. **Calculating Embeddings**: Once you have a Word2Vec model loaded, you can use it to calculate word embeddings for your text data. This involves converting each word in a piece of text into its corresponding vector representation using the Word2Vec model. You can then combine these word vectors to obtain a single vector representation for the entire text.

3. **Computing Similarity**: With the embeddings calculated for both the user input and your dataset, you can compute similarity between them using a similarity metric such as cosine similarity. Cosine similarity measures the cosine of the angle between two vectors and provides a value between -1 and 1, where higher values indicate greater similarity.

4. **Finding the Most Similar Data Points**: After computing similarity scores between the user input and each data point in your dataset, you can identify the most similar data points (e.g., laws) by selecting those with the highest similarity scores.

Overall, loading a Word2Vec model separately in your action code allows you to leverage word embeddings to compute similarity between user input and your dataset, enabling tasks such as retrieving the most relevant data points based on user queries.

-----------------------------------------------------------------

The configuration you provided in `config.yml` specifies the use of the Hugging Face Transformers NLP component (`HFTransformersNLP`) with the Word2Vec model (`google/word2vec-google-news-300`) for feature extraction. This configuration will indeed change the behavior of your NLU pipeline, but it won't directly enable computing similarity between user input and your dataset.

Here's what happens with this configuration:

1. **HFTransformersNLP Component**: The `HFTransformersNLP` component uses pre-trained language models from Hugging Face's model hub. In this case, you're specifying the Word2Vec model (`google/word2vec-google-news-300`). However, it's important to note that the Word2Vec model is not a Transformer-based model like BERT or GPT, which are commonly used with the `HFTransformersNLP` component. Therefore, using the Word2Vec model with this component might not provide optimal results because the component is designed for Transformer-based models.

2. **LanguageModelTokenizer and LanguageModelFeaturizer**: These components tokenize the input text and extract features from it using the specified language model. Since Word2Vec is not a Transformer-based model, these components may not be able to tokenize the input text and extract features properly.

To compute similarity between user input and your dataset using a Word2Vec model, you typically need to:

- Load the Word2Vec model separately in your custom action code.
- Preprocess the user input and compute embeddings for it using the Word2Vec model.
- Compute similarity between the user input embeddings and the embeddings of your dataset.

Changing the configuration in `config.yml` alone won't handle these tasks. You would still need to implement the similarity computation logic in your custom action code, as shown in previous examples.
