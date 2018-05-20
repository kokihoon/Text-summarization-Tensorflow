# -*- coding:utf-8 -*-
import hanja
import konlpy
import csv


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
                 remove_construction=True):
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
        if remove_construction:
            self._convert_func_list.append(SentencePreProcessing.remove_unnecessary_construction)

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
    def remove_unnecessary_construction(sentence):
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


def make_dictionary():
    """
    학습과 테스트를 위한 단어 리스트들 저장
    :return:
    """
    pass

if __name__ == '__main__':
    # Test Code
    test = SentenceToTokenizer()
    t = test.convert('北 이르면 열흘후 풍계리 핵실험장 폭파…생중계 안할듯')
    print(t)
    t = test.convert('北 이르면 열흘후 풍계리 핵실험장 폭파…생중계 안할듯')
    print(t)
