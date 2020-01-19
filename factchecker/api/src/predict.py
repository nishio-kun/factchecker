import collections
import os
import traceback

import MeCab
import numpy as np
import tensorflow as tf


tagger = MeCab.Tagger('-Ochasen')

MONOGRAM_KEYS = os.getenv('MONOGRAM_KEYS')
BIGRAM_KEYS = os.getenv('BIGRAM_KEYS')


def monogramize(txt):
    poses = []
    poses_simple = []
    words = []
    for tok in tagger.parse(txt).split('\n'):
        d = tok.split('\t')
        if len(d) == 1:
            continue
        poses.append(d[3])  #品詞
        poses_simple.append(d[3].split('-')[0])
        words.append(d[0])  #単語（基本形）
    return poses_simple, words


def bigramize(L):
    return [L[i] + '-' + L[i + 1] for i in range(len(L) - 1)]


def make(poses, words):
    auxiliary_verbs = [
            'た', 'だ', 'ない', 'う', 'です', 'ます', 'な', 'ある', 'で',
            'ん', 'たい', 'だろ', 'だっ',]# 'ぬ', 'らしい', 'たら', 'なかっ', 'まし', 'なら']
    particles = ['の', 'に', 'は', 'て', 'を', 'が', 'と', 'で',]# 'も', 'か', 'から', 'よ', 'な', 'ば', 'ね', 'って', 'という', 'まで', 'だけ', 'じゃ', 'へ', 'けど', 'わ', 'ながら', 'や', 'ので', 'として', 'でも', 'し', 'なんて', 'より', 'ぞ', 'とか', 'のに', 'など', 'かも', 'ほど', 'くらい', 'しか', 'ばかり', 'たり', 'だって']
    symbols = ['、', '。', '「', '」', '…', '！', '？', '\u3000', '─', '『', '』','（', '）']
    for i, (p, w) in enumerate(zip(poses, words)):
        if w in auxiliary_verbs + particles + symbols:
            poses[i] = words[i]

    L = []
    monogram = collections.Counter(poses)
    total = sum(monogram.values())
    path = MONOGRAM_KEYS
    with open(path, encoding='utf-8_sig') as f:
        for pos, num in [x.strip().split(',') for x in f.readlines()]:
            num = int(num)
            try:
                L.append(monogram[pos] / total)
            except:
                traceback.print_exc()
                L.append(0.0)

    bigram = collections.Counter(bigramize(poses))
    total = sum(bigram.values())
    path = BIGRAM_KEYS
    with open(path, encoding='utf-8_sig') as f:
        for pos2, num in [x.strip().split(',') for x in f.readlines()]:
            num = int(num)
            try:
                L.append(bigram[pos2] / total)
            except:
                traceback.print_exc()
                L.append(0.0)

    return L


def predict(sentences, model):
    vects = []

    for sentence in sentences:
        k1, k2 = monogramize(sentence)
        vects.append(make(k1, k2))

    model = tf.keras.models.load_model(model)

    predicts = model.predict(np.array(vects))
    return predicts


def labeling(label, sentences, predicts):
    ret = []
    for sentence, result in zip(sentences, predicts):
        ret.append(
                {'sentence': sentence, 'distinction': label[result.argmax()]})
    return ret
