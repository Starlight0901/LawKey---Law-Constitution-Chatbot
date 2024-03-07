from transformers import pipeline
import nltk

from utils.nlpUtils import law_cleaning

model_name = "google/flan-t5-base"

# Initialize the summarization pipeline
summarization_pipeline = pipeline("summarization", model=model_name, tokenizer=model_name)


# def analyze_complexity(text):
#     """
#     Calculates a basic complexity score for a legal document using NLTK.
#     This function can be further improved by incorporating additional metrics
#     or a weighted combination of metrics.
#     """
#     tokens = nltk.word_tokenize(text)
#     num_sentences = len(nltk.sent_tokenize(text))
#     avg_sentence_length = len(tokens) / num_sentences if num_sentences > 0 else 0
#     flesch_kincaid_grade = 0.39 * avg_sentence_length / 11.8 + 16.9 * 100 / (
#             num_sentences * avg_sentence_length)  # Flesch-Kincaid grade level
#
#     # Combine metrics into a single score (adjust weights as needed)
#     complexity_score = (avg_sentence_length + flesch_kincaid_grade) / 2
#
#     return complexity_score


def summarize_laws_with_t5(laws, min_length=5, max_length=50):
    # preprocessed_law = law_cleaning(laws) if law_cleaning else laws
    summarized_laws = {}
    for law in laws:
        # Generate summary using the pipeline
        # complexity_score = analyze_complexity(preprocessed_law)
        # min_length = max(min_length, int(complexity_score * 0.5))
        # max_length = min(max_length, int(complexity_score * 1.2))
        #
        # summary = summarization_pipeline("Summarize: " + law,
        #                                  max_length=max_length,
        #                                  min_length=min_length)[0]['summary_text']

        summary = summarization_pipeline("Summarize: " + law, max_length=50, min_length=5, do_sample=False)[0]['summary_text']
        summarized_laws[law] = summary
    return summarized_laws
