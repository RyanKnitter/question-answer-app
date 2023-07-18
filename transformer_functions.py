from transformers import pipeline

def question_answer(question, context, model_name = "microsoft/xdoc-base-squad2.0"):
    model = pipeline('question-answering', model=model_name, tokenizer=model_name)
    QA_input = {
        'question': question,
        'context': context
    }
    return model(QA_input).get('answer')