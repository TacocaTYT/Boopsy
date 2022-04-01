from random_word import RandomWords
rw = RandomWords()

word = "7"
for i in "aaaaaaaaaa":
    word = str(rw.get_random_word(minLength=5,hasDictionaryDef="true",excludePartOfSpeech="noun,pronoun,verb")).lower()
    while " " in word or "-" in word:
        word = str(rw.get_random_word(minLength=5,hasDictionaryDef="true",excludePartOfSpeech="noun,pronoun,verb")).lower()
    print(word)