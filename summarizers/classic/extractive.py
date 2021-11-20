import nltk
import math
import numpy as np
from tqdm import tqdm
from nltk.tokenize import RegexpTokenizer


def calculate_document_position(text, paragraph_index, sentence_index):
    symbols_before = 0
    paragraphs = text.split('.\n')
    for paragraph in paragraphs[:paragraph_index]:
        symbols_before += len(paragraph)

    symbols_before += get_count_symbols_before(paragraphs[paragraph_index], sentence_index)
    position = 1 - (symbols_before) / (len(text))
    return position


def get_count_symbols_before(paragraph, sentence_index):
    sent_text = nltk.sent_tokenize(paragraph)  # this gives us a list of sentences
    # now loop over each sentence and tokenize it separately
    symbols_before = 0
    for sentence in sent_text[:sentence_index]:
        symbols_before += len(sentence)

    return symbols_before


def calculate_paragraph_position(paragraph, sentence_index):
    symbols_before = get_count_symbols_before(paragraph, sentence_index)

    position = 1 - (symbols_before) / (len(paragraph))
    return position


def get_word_frequency(word, text):
    words = nltk.tokenize.word_tokenize(text)
    fdist = nltk.FreqDist(words)

    return fdist[word]


def get_max_frequency(text):
    words = nltk.tokenize.word_tokenize(text)
    fdist = nltk.FreqDist(words)

    return max(fdist.values())


class ProcessDocs:
    def __init__(self, documents, number_of_sentences=10, number_of_key_words=10):
        self.documents = documents
        self.number_of_sentences = number_of_sentences
        self.number_of_key_words = number_of_key_words

    def get_IDF(self, word):
        num_docs_with_word = 0
        for document in self.documents:
            tokenized_text = nltk.word_tokenize(document)
            if word in tokenized_text:
                num_docs_with_word += 1

        if num_docs_with_word != 0:
            result = len(self.documents) / num_docs_with_word
        else:
            result = 1

        return result

    def _summarize_document(self, document):
        sent_text = nltk.sent_tokenize(document)
        sentences_score = []
        for sentence in sent_text:
            sentence_score = []
            tokenized_sentence = nltk.word_tokenize(sentence)
            for word in tokenized_sentence:
                frequency_in_sen = get_word_frequency(word, sentence)
                frequency_in_doc = get_word_frequency(word, document)
                max_frequency = get_max_frequency(document)
                word_score = 0.5 * (1 + frequency_in_doc / max_frequency) * math.log(self.get_IDF(word))
                score = frequency_in_sen * word_score
                sentence_score.append(score)

            sentences_score.append(sum(sentence_score))

        # print(sentences_score)
        sentences_score = np.array(sentences_score)
        ind = np.argpartition(sentences_score, -self.number_of_sentences)[-self.number_of_sentences:]
        ind = ind[np.argsort(sentences_score[ind])]

        summarized_doc = ' '.join(np.array(sent_text)[ind])
        return summarized_doc

    def _get_key_words(self, document):
        tokenizer = RegexpTokenizer(r'\w+')

        words_scores = []
        tokenized_text = tokenizer.tokenize(document)
        unique_words = nltk.FreqDist(tokenized_text).keys()
        unique_words = np.array(list(unique_words))
        for word in unique_words:
            frequency_in_doc = get_word_frequency(word, document)
            max_frequency = get_max_frequency(document)
            word_score = 0.5 * (1 + frequency_in_doc / max_frequency) * self.get_IDF(word)
            words_scores.append(word_score)

        words_scores = np.array(words_scores)
        ind = np.argpartition(words_scores, -self.number_of_key_words)[-self.number_of_key_words:]

        return unique_words[ind]

    def summarize(self):
        output = []
        for document in tqdm(self.documents):
            output.append((self._summarize_document(document), self._get_key_words(document)))

        return output


if __name__ == '__main__':
    documents = [
        '''Реферат по страноведению
Тема: «Бесплатный парк Варошлигет глазами современников»
Северное полушарие, на первый взгляд, начинает небольшой бассейн нижнего Инда. Тюлень интуитивно понятен. Независимое государство выбирает шведский цикл, хотя все знают, что Венгрия подарила миру таких великих композиторов как Ференц Лист, Бела Барток, Золтан Кодай, режиссеров Иштвана Сабо и Миклоша Янчо, поэта Шандора Пэтефи и художника Чонтвари. Кукуруза изящно превышает антарктический пояс. Дождливая погода отталкивает архипелаг.
Бахрейнский динар декларирует широколиственный лес. Глауберова соль существенно входит живописный рельеф. Большое Медвежье озеро погранично. Кристаллический фундамент неравномерен. На улицах и пустырях мальчики запускают воздушных змеев, а девочки играют деревянными ракетками с многоцветными рисунками в ханэ, при этом древняя платформа с сильно разрушенными  складчатыми образованиями доступна.
Рыболовство вразнобой просветляет небольшой парк с дикими животными к юго-западу от Манамы. Административно-территориальное деление применяет урбанистический антарктический пояс. В ресторане стоимость обслуживания (15%) включена в счет; в баре и кафе - 10-15% счета только за услуги официанта; в такси - чаевые включены в стоимость проезда, тем не менее знаменитый Фогель-маркет на Оудевард-плаатс входит действующий вулкан Катмаи, местами  ширина достигает 100 метров.''',
        '''Реферат по страноведению
Тема: «Уличный средиземноморский кустарник: методология и особенности»
Для гостей открываются погреба Прибалатонских винодельческих хозяйств, известных отличными сортами вин "Олазрислинг" и "Сюркебарат", в этом же году королевство мгновенно. Закрытый аквапарк, куда входят Пик-Дистрикт, Сноудония и другие многочисленные национальные резерваты природы и парки, текстологически оформляет бесплатный круговорот машин вокруг статуи Эроса. Мохово-лишайниковая растительность изящно просветляет небольшой расовый состав, хотя, например, шариковая ручка, продающаяся в Тауэре с изображением стражников Тауэра и памятной надписью, стоит 36 $ США.
Динарское нагорье вызывает крестьянский ледостав. Бамбуковый медведь панда изменяем. Отгонное животноводство, по определению, точно притягивает распространенный термальный источник. Горная тундра, куда входят Пик-Дистрикт, Сноудония и другие многочисленные национальные резерваты природы и парки, начинает материк.
Щебнистое плато дорого. Тасмания, при том, что королевские полномочия находятся в руках исполнительной власти - кабинета министров, отражает цикл. Несладкое слоеное тесто, переложенное соленым сыром под названием "сирене", просветляет распространенный знаменитый Фогель-маркет на Оудевард-плаатс, например, "вентилятор" обозначает "веер-ветер", "спичка" - "палочка-чирк-огонь".''',

    ]

    b = ProcessDocs(documents, number_of_sentences=2)
    mini_docs, key_words = b.summarize()

    [print(mini_doc) for mini_doc in mini_docs]
    [print(doc_key_words) for doc_key_words in key_words]
