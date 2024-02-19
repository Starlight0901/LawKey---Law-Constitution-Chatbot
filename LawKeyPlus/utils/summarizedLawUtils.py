from transformers import pipeline

model_name = "google/flan-t5-base"

# Initialize the summarization pipeline
summarization_pipeline = pipeline("summarization", model=model_name, tokenizer=model_name)


def summarize_laws_with_t5(laws):
    summarized_laws = {}
    for law in laws:
        # Generate summary using the pipeline
        summary = summarization_pipeline("Summarize: " + law, max_length=50, min_length=5, do_sample=False)[0]['summary_text']
        summarized_laws[law] = summary
    return summarized_laws
