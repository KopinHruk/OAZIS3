from summarizers.classic.extractive import ProcessDocs
from summarizers.ml.abstract import get_abstract_summary
from summarizers.ml.extractive import get_extractive_summary


def process(documents, config):
    if config['type'] == 'classic':
        object = ProcessDocs(documents, number_of_sentences=config['number_of_sentences'], number_of_key_words=config['number_of_key_words'])
        output = object.summarize()

        return output


    else:
        output = []
        for document in documents:
            abstract_summary = get_abstract_summary(document)
            extractive_summary = get_extractive_summary(document, number_of_sentences=config['number_of_sentences'])
            output.append((document, abstract_summary, extractive_summary))


        return output