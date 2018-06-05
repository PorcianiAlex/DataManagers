from PersonalityInsight.process_data import build_data_cv, load_bin_vec, add_unknown_words, get_W, get_mairesse_features
from PersonalityInsight.conv_net_train import make_idx_data_cv, train_conv_net, Sigmoid
import PersonalityInsight
import pandas as pd
import numpy as np
import pickle as pk
import csv
import sys

def ProcessDataMain(wordVector, dataset, mairesse):
    w2v_file = wordVector
    data_folder = dataset
    mairesse_file = mairesse
    print("loading data..."),
    revs, vocab = build_data_cv(data_folder, cv=10, clean_string=True)
    num_words = pd.DataFrame(revs)["num_words"]
    max_l = np.max(num_words)
    print("data loaded!")
    print("number of status: " + str(len(revs)))
    print("vocab size: " + str(len(vocab)))
    print("max sentence length: " + str(max_l))
    print("loading word2vec vectors..."),
    w2v = load_bin_vec(w2v_file, vocab)
    print("word2vec loaded!")
    print("num words already in word2vec: " + str(len(w2v)))
    add_unknown_words(w2v, vocab)
    W, word_idx_map = get_W(w2v)
    rand_vecs = {}
    add_unknown_words(rand_vecs, vocab)
    W2, _ = get_W(rand_vecs)
    mairesse = get_mairesse_features(mairesse_file)
    pk.dump([revs, W, W2, word_idx_map, vocab, mairesse], open("essays_mairesse.p", "wb"))
    print("dataset created!")

def ConvNetTrainMain(mode, wordVec, attr):
    print("loading data..."),
    x = pk.load(open("essays_mairesse.p", "rb"))
    revs, W, W2, word_idx_map, vocab, mairesse = x[0], x[1], x[2], x[3], x[4], x[5]
    print("data loaded!")
    mode = mode
    word_vectors = wordVec
    attr = attr
    if mode == "-nonstatic":
        print("model architecture: CNN-non-static")
        non_static = True
    elif mode == "-static":
        print("model architecture: CNN-static")
        non_static = False
        PersonalityInsight.conv_net_classes.run  # execfile("conv_net_classes.py")
    if word_vectors == "-rand":
        print("using: random vectors")
        U = W2
    elif word_vectors == "-word2vec":
        print("using: word2vec vectors")
        U = W

    r = range(0, 10)

    ofile = open('perf_output_' + str(attr) + '.txt', 'w')

    charged_words = []

    emof = open("PersonalityInsight\Emotion_Lexicon.csv", "r")
    csvf = csv.reader(emof, delimiter=',', quotechar='"')
    first_line = True

    for line in csvf:
        if first_line:
            first_line = False
            continue
        if line[11] == "1":
            charged_words.append(line[0])

    emof.close()

    charged_words = set(charged_words)

    results = []
    for i in r:
        datasets = make_idx_data_cv(revs, word_idx_map, mairesse, charged_words, i, attr, max_l=149, max_s=312, k=300,
                                    filter_h=3)

        perf, fscore = train_conv_net(datasets,
                                      U,
                                      ofile,
                                      cv=i,
                                      attr=attr,
                                      lr_decay=0.95,
                                      filter_hs=[1, 2, 3],
                                      conv_non_linear="relu",
                                      hidden_units=[200, 200, 2],
                                      shuffle_batch=True,
                                      n_epochs=50,
                                      sqr_norm_lim=9,
                                      non_static=non_static,
                                      batch_size=50,
                                      dropout_rate=[0.5, 0.5, 0.5],
                                      activations=[Sigmoid])
        output = "cv: " + str(i) + ", perf: " + str(perf) + ", macro_fscore: " + str(fscore)
        print(output)
        ofile.write(output + "\n")
        ofile.flush()
        results.append([perf, fscore])
    results = np.asarray(results)
    perf_out = 'Perf : ' + str(np.mean(results[:, 0]))
    fscore_out = 'Macro_Fscore : ' + str(np.mean(results[:, 1]))
    print(perf_out)
    print(fscore_out)
    ofile.write(perf_out + "\n" + fscore_out)
    ofile.close()

def Main():
    #wordVector = 'C:\\Users\\gabri\Desktop\\Ingegneria\\Magistrale\\First Year\\Second Semester\\DataManagers\\GoogleNews-vectors-negative300.bin'
    #dataset = 'PersonalityInsight/essays.csv'
    #mairesse = 'PersonalityInsight/mairesse.csv'
    #ProcessDataMain(wordVector, dataset, mairesse)

    wordVector = "-word2vec"
    mode = "-nonstatic"
    attr = 2
    attr = np.int32(attr)
    ConvNetTrainMain(mode, wordVector, attr)


Main()