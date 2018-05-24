# -*- coding:utf-8 -*-
import collections
import hanja
import konlpy
import csv
import time
import pickle
import os


class PreProcessing(object):
    """
    데이터 전처리를 위한 최상위 클래스
    """
    def __init__(self):
        self._convert_func_list = list()    # 데이터 전처리를 위한 힘수들을 모아놓는 리스트

    def convert(self, sentence):
        """
        convert_func_list 에 저장되어 있는 전처리 함수들을 문장에 적용하여 문장을 적절히 전처리
        :param sentence: 문장 (type: str)
        :return: 변환된 문장 (type: str)
        """
        result = sentence
        for func in self._convert_func_list:
            result = func(result)
        return result


class SentenceToTokenizer(PreProcessing):
    """
    한글로 된 문장을 적절히 토큰나이즈 해주는 기능들을 모아놓은 클래스
    """
    def __init__(self,
                 remove_tag_list=None,
                 norm=False,
                 stem=False):
        """

        한글로 된 문장을 적절히 토큰나이즈 해주는 기능을 제공

        :param remove_tag_list: 제거한 Pos Tag list (type: list)
        :param norm: 단어를 정규화
            ex) 입니닼ㅋㅋ -> 입니다 ㅋㅋ, 샤릉해 -> 사랑해

        :param stem: 어근화를 실시
            ex) 한국어를 처리하는 예시입니다 ㅋㅋ -> 한국어, 를, 처리, 하다, 예시, 이다, ㅋㅋ
            (하는 -> 하다, 입니다 -> 이다)
        """
        super(SentenceToTokenizer, self).__init__()
        if not remove_tag_list:
            self._remove_tag_list = list()
        else:
            self._remove_tag_list = remove_tag_list
        self._norm = norm
        self._stem = stem
        self._tokenizer = konlpy.tag.Twitter()
        self._convert_func_list.append(self.sentence_tokenizer)

    def sentence_tokenizer(self, sentence):
        """
        :param self:
        :param sentence:
        :return:
        """
        tokens = self._tokenizer.pos(sentence, norm=self._norm, stem=self._stem)
        tokens = [token[0] for token in tokens if token not in self._remove_tag_list]
        return tokens


class SentencePreProcessing(PreProcessing):
    """
    네이버에서 받아온 한글 신문 문장들을 전처리하는 기능을을 모아놓은 클래스
    """
    def __init__(self,
                 convert_hanja=True,
                 clearning_sentence=True):
        """
        문장들을 사용자가 정한대로 전처리 하는 기능

        예)
        1. self._convert_hanja = True, self._remove_construction = False
          : 문장을 입력받아 한자로 입력된 글자는 한글로 변환

        2. self._convert_hanja = True, self._remove_construction = Ture
          : 문장을 입력받아 한자로 입력된 글자를 한글로 변환하고 쓸모없는 구문들은 제거

        :param convert_hanja: 참이면 한자를 한글로 변환 (type: Boolean)
        :param remove_construction: 참이면 쓸모없는 구문들을 제거 (type: Boolean)
        """
        super(SentencePreProcessing, self).__init__()
        if convert_hanja:
            self._convert_func_list.append(SentencePreProcessing.convert_hanja_to_hangul)
        if clearning_sentence:
            self._convert_func_list.append(SentencePreProcessing.cleaning_sentence)

    @staticmethod
    def convert_hanja_to_hangul(sentence):
        """
        문장안에 한자가 포함되어 있으면 한글로 변화시켜주는 기능

        예)
        1. 北 이르면 열흘후 풍계리 핵실험장 폭파…생중계 안할듯 -> 북 이르면 열흘후 풍계리 폭파…생중계 안할듯
        2. 靑 北풍계리 폐기 최소한 미래엔 핵개발 않겠다는 의미종합 -> 청 북계리 폐기 최소한 미래엔 핵개발 않겠다는 의미종합

        :param sentence: 문장 (type: str)
        :return: 변환된 문장 (type : str)
        """
        sentence = hanja.translate(sentence, 'substitution')
        return sentence

    @staticmethod
    def cleaning_sentence(sentence):
        # TODO : 문장에 있는 쓸모없는 구문 제거 기능 구현
        """
        문장안에 쓸모없는 구문들과 문자들을 제거하는 기능

        예)

        1. 기사이름, 신문사이름 제거 : 서울뉴스1 조소영 기자박승주 기자 청와대는 북한이 오는 23일부터 ... -> 청화대는 북한이 오는 23일 부터 ...
        2. 쓸모없는 문구 제거 : 그는 전날에도 국회 본청 앞 단식농성장에서 호흡곤란과 가슴 통증을 호소하였다 ⓒ 무단전재 및 재배포금지
                                -> 그는 전날에도 국회 본청 앞 단식농성장에서 호흡곤란과 가슴 통증을 호소하였다

        :param sentence: 문장 (type: str)
        :return: 변환된 문장 (type : str)
        """
        return sentence


class SentenceConverter(object):
    def __init__(self,
                 pre_processor,
                 tokenizer):
        self.__pre_processor = pre_processor
        self.__tokenizer = tokenizer

    def get_convert_func(self):
        return lambda sentence: self.__tokenizer.convert(self.__pre_processor.convert(sentence))


'======================================================================================================================'
'======================================================================================================================'
'======================================================================================================================'


_UNK_ = '_UNK_'     # 알수없는 단어를 표시하기 위한 mask (단어장에 존재 하지 않는 단어)
_PAD_ = '_PAD_'     # 길이를 맞춰주기 위한 mask
_GO_ = '_GO_'       # 문장의 시작을 알려주기위한 mask
_END_ = '_END_'     # 문장의 끝을 알려구기위한 mask
unk_id = 0          # _UNK_ number id
pad_id = 1          # _PAD_ number id
go_id = 2           # _GO_  number id
end_id = 3          # _EMD_ number id
MASK_INFO = {
    _UNK_: unk_id,
    _PAD_: pad_id,
    _GO_: go_id,
    _END_: end_id
}


def make_dictionary(
        file_path_list,
        save_point,
        sentence_converter_func,
        word_max_count):
    """
    학습/테스트에 필요한 단어 리스트, word2idx 사전, idx2word 사전를 만들어주는 기능

    1. vocab : ['단어1', '단어2', ...]
    2. word2idx : {'단어1' : 번호1, '단어2' : 번호2}          \
    3. idx2word : {번호1 : '단어1', 번호2 : '단어2'}

    :param file_path_list: 데이터셋 path 리스트 (type: list)
    :param save_point: 결과물을 저장할 디렉토리 위치 (type: str)
    :param sentence_converter_func: 데이터셋의 문장을 전처리하기 위한 lambda function  (type: func)
    :return: vocabulary_path, word2idx_path, idx2word_path
        vocabulary_path : 단어장 저장 위치
        word2idx_path : word2idx 저장 위치
        idx2word_path : idx2word 저장 위치
    """

    start_time = time.time()

    # 결과물들을 저장할 파일 생성
    if not os.path.exists(save_point):
        abs_save_path = os.path.abspath(save_point)
        os.makedirs(abs_save_path)
    if not os.path.exists(os.path.join(save_point, 'dict')):
        abs_save_path = os.path.abspath(os.path.join(save_point, 'dict'))
        os.makedirs(abs_save_path)

    # 파일이름
    vocabulary_path = os.path.join(save_point, 'vocabulary.txt')
    word2idx_path = os.path.join(save_point, 'dict', 'word2idx.dic')
    idx2word_path = os.path.join(save_point, 'dict', 'idx2word.dic')

    # 파일 포인트
    vocabulary_fp = open(vocabulary_path, 'w', encoding='utf-8')
    word2idx_fp = open(word2idx_path, 'wb')
    idx2word_fp = open(idx2word_path, 'wb')

    # 단어 리스트 생성
    words = set()
    for file_path in file_path_list:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = sentence_converter_func(row['title'])
                content = sentence_converter_func(row['content'])
                words = words.union(set(title))
                words = words.union(set(content))

    vocab = list(MASK_INFO.keys())      # 단어장에 '_UNK_', '_PAD_', '_GO_', '_END_' 추가
    words = list(words)
    words.sort()                        # 네이버 뉴스 단어 리스트 정렬

    # 단어의 출현횟수가 word_max_count 보다 많으면 단어목록에서 삭제
    counter = collections.Counter(words)
    words = [word for word, num in counter.items() if num < word_max_count]

    # 단어장에서 네이버 뉴스 단어 리스트 추가
    vocab.extend(words)

    print('단어 리스트 완성...')

    word2idx = dict()
    idx2word = dict()
    for i, word in enumerate(vocab):
        vocabulary_fp.write(str(word) + '\n')    # vocabulary.txt 에 단어 리스트 저장
        idx2word[i] = word
        word2idx[word] = i
    pickle.dump(word2idx, word2idx_fp)          # word2idx.dic 에 딕셔너리 저장
    pickle.dump(idx2word, idx2word_fp)          # idx2word.dic 에 딕셔너리 저장

    vocabulary_fp.close()
    word2idx_fp.close()
    idx2word_fp.close()

    end_time = time.time()
    diff_time = round(end_time - start_time, 3)

    print('단어장/사전 저장 완료... 총 걸린 시간 : {} sec, 총 단어 갯수 : {}'.format(diff_time, len(words)))
    return vocabulary_path, word2idx_path, idx2word_path

'======================================================================================================================'
'======================================================================================================================'
'======================================================================================================================'


class ParentBachIter(object):
    def __init__(self,
                 data_paths,
                 epochs,
                 batch_size,
                 word2idx_path,
                 idx2word_path,
                 sentence_converter_func):
        self.data_paths = data_paths
        self.epochs = epochs
        self.batch_size = batch_size
        self.word2idx_path = word2idx_path
        self.idx2word_path = idx2word_path
        self.sentence_converter_func = sentence_converter_func
        self.word2idx, self.idx2word = self._load_dictionary()

    def _load_dictionary(self):
        """
        word2idx.dic, idx2word.dic 사전 데이터 불러오는 기능
        :return: word2idx.dic, idx2word.dic
        """

        # word2idx.dic, idx2word.dic 파일이 존재하는지 확인
        if not os.path.exists(self.word2idx_path) or not os.path.exists(self.idx2word_path):
            raise FileExistsError

        # 사전 파일 로드
        word2idx = pickle.load(open(self.word2idx_path, 'rb'))
        idx2word = pickle.load(open(self.idx2word_path, 'rb'))
        return word2idx, idx2word

    def _get_data_set(self):
        for data_path in self.data_paths:
            print(data_path)
        pass

    def next_batches(self):
        pass


class Word2VecModelBatchIter(ParentBachIter):
    def __init__(self,
                 data_paths,
                 epochs,
                 batch_size,
                 window_size,
                 word2idx_path,
                 idx2word_path,
                 sentence_converter_func):
        super(Word2VecModelBatchIter, self).__init__(
            data_paths=data_paths,
            epochs=epochs,
            batch_size=batch_size,
            word2idx_path=word2idx_path,
            idx2word_path=idx2word_path,
            sentence_converter_func=sentence_converter_func
        )
        self.window_size = window_size


class SummaryModelBatchIter(ParentBachIter):
    def __init__(self,
                 data_paths,
                 epochs,
                 batch_size,
                 word2idx_path,
                 idx2word_path,
                 sentence_converter_func):
        super(SummaryModelBatchIter, self).__init__(
            data_paths=data_paths,
            epochs=epochs,
            batch_size=batch_size,
            word2idx_path=word2idx_path,
            idx2word_path=idx2word_path,
            sentence_converter_func=sentence_converter_func
        )

    def next_batches(self):
        pass


if __name__ == '__main__':
    pre_processor_inst = SentencePreProcessing(
        convert_hanja=True,
        clearning_sentence=True
    )
    tokenizer = SentenceToTokenizer(
        norm=True,
        stem=True
    )
    converter_func = SentenceConverter(
        tokenizer=tokenizer,
        pre_processor=pre_processor_inst
    ).get_convert_func()

    make_dictionary(
        file_path_list=['./data/navernews_data.csv'],
        save_point='./data/words',
        sentence_converter_func=converter_func,
        word_max_count=20
    )

    SummaryModelBatchIter(
        data_paths=['./data/navernews_data.csv'],
        epochs=1,
        batch_size=10,
        window_size=2,
        word2idx_path='./data/words/dict/word2idx.dic',
        idx2word_path='./data/words/dict/idx2word.dic',
        sentence_converter_func=converter_func
    )
    #
    # def test():
    #     n = 0
    #     while n < 3:
    #         n += 1
    #         yield n
    #
    # t = test()
    # while True:
    #     try:
    #         print(next(t))
    #     except StopIteration:
    #         print('end')
    #         break




