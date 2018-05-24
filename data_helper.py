# -*- coding:utf-8 -*-
import hanja
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
        for func in self._convert_func_list:
            sentence = func(sentence)
        return sentence


class SentenceToTokenizer(PreProcessing):
    """
    한글로 된 문장을 적절히 토큰나이즈 해주는 기능들을 모아놓은 클래스
    """
    def __init__(self):
        super(SentenceToTokenizer, self).__init__()

    @staticmethod
    def remove_unnecessary_tags(words, remove_tag_list):
        # TODO : 불필요한 테그 리스트들을 입력받아 해당하는 태그를 가진 단어들을 제거하는 기능 구현
        # TODO : remove_unnecessary_tags 기능에 대한 상세한 설명 추가
        """
        :param words:
        :param remove_tag_list:
        :return:
        """
        pass

    @staticmethod
    def normalization_words(words):
        # TODO : 단어를 표준화하는 기능 구현
        # TODO : normalization_words 기능에 대한 상세한 설명 추가
        """
        :param words:
        :return:
        """
        pass


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
        # TODO : 문장에 있는 한자를 한글로 변환기켜주는 기능 구현
        """
        문장안에 한자가 포함되어 있으면 한글로 변화시켜주는 기능

        예)
        1. 北 이르면 열흘후 풍계리 핵실험장 폭파…생중계 안할듯 -> 북 이르면 열흘후 풍계리 폭파…생중계 안할듯
        2. 靑 北풍계리 폐기 최소한 미래엔 핵개발 않겠다는 의미종합 -> 청 북계리 폐기 최소한 미래엔 핵개발 않겠다는 의미종합

        :param sentence: 문장 (type: str)
        :return: 변환된 문장 (type : str)
        """
        return hanja.translate(sentence, 'substitution')

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
        if "기자" in sentence :
            sentence = sentence.split("기자")[-1]
        if "ⓒ" in sentence :
            sentence = sentence.split('ⓒ')[0]

        return sentence


def make_dictionary():
    """
    학습과 테스트를 위한 단어 리스트들 저장
    :return:
    """
    pass

if __name__ == '__main__':
    # Test Code
    test = SentencePreProcessing()
    t = test.convert('서울뉴스1 조소영 기자박승주 기자 청와대는 북한이 오는 23일부터 ...')
    print(t)