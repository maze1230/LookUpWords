class Word:
    def __init__(self,
                 name,
                 mean=None,
                 synonym=None,
                 sentence_en=None,
                 sentence_ja=None):
        self.name = name
        self.mean = mean
        self.synonym = synonym
        self.sentence_en = sentence_en
        self.sentence_ja = sentence_ja

    def to_csv(self):
        return [
            self.name, ','.join(self.mean), ','.join(self.synonym),
            self.sentence_en, self.sentence_ja
        ]
