from transformers import pipeline
import math
from langdetect import detect_langs

def get_abstract_summary(text):
    scores = detect_langs(text)
    if scores[0].lang == 'ru':
        summarizer = pipeline("summarization", model='IlyaGusev/mbart_ru_sum_gazeta')
    else:
        summarizer = pipeline("summarization")


    max_embedding = 1024*3

    summary_text_full = ''
    num = math.ceil(len(text) / max_embedding)
    for i in range(num):
        start = i*max_embedding
        end = (i+1)*max_embedding

        summary_text = summarizer(text[start:end][:1024], max_length=1024, min_length=35, do_sample=False)
        summary_text = summary_text[0]['summary_text']
        summary_text_full += summary_text

    return summary_text_full


if __name__ == '__main__':
    text1 = """One month after the United States began what has become a troubled rollout of a national COVID 
    vaccination campaign, the effort is finally gathering real steam. Close to a million doses -- over 951,000, 
    to be more exact -- made their way into the arms of Americans in the past 24 hours, the U.S. Centers for Disease 
    Control and Prevention reported Wednesday. That's the largest number of shots given in one day since the rollout 
    began and a big jump from the previous day, when just under 340,000 doses were given, CBS News reported. That 
    number is likely to jump quickly after the federal government on Tuesday gave states the OK to vaccinate anyone 
    over 65 and said it would release all the doses of vaccine it has available for distribution. Meanwhile, 
    a number of states have now opened mass vaccination sites in an effort to get larger numbers of people 
    inoculated, CBS News reported. """

    text2 = '''А русский язык? - спросил Крапивин. -Он работает, на счет этого можете не переживать. Все будет в лучшем
            виде! - Ответил Влад.'''

    temp = get_abstract_summary(text1)
    print(temp)
