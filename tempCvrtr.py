from random_word import RandomWords
rw = RandomWords()
for i in "aaaaaaaaaa":
    print(str(rw.get_random_word(minLength=5,hasDictionaryDef="true",excludePartOfSpeech="noun,pronoun,verb")).lower())