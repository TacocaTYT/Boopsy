from random_word import RandomWords
rw = RandomWords()
<<<<<<< HEAD

word = "7"
for i in "aaaaaaaaaa":
    word = str(rw.get_random_word(minLength=5,hasDictionaryDef="true",excludePartOfSpeech="noun,pronoun,verb")).lower()
    while " " in word or "-" in word:
        word = str(rw.get_random_word(minLength=5,hasDictionaryDef="true",excludePartOfSpeech="noun,pronoun,verb")).lower()
    print(word)
=======
for i in "aaaaaaaaaa":
    print(str(rw.get_random_word(minLength=5,hasDictionaryDef="true",excludePartOfSpeech="noun,pronoun,verb")).lower())
>>>>>>> 79a16447ed7ca9ce1f0c1c9b3ed499a90ad2728b
