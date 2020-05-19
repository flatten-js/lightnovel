import re
import MeCab
import sqlite3
from collections import defaultdict
from typing import List, Dict, Tuple

class Model(object):
    """
    Form a morpheme model for Markov chain

    Attributes
    ----------
    BEGIN : str
        Beginning of sentence
    END : str
        End of sentence
    DB_PATH : str
        Path to DB file
    DB_SCHEMA_PATH : str
        Path to the sql file that contains schema information
    """

    BEGIN = "__BEGIN_SENTENCE__"
    END = "__END_SENTENCE__"

    DB_PATH = "./db/model.db"
    DB_SCHEMA_PATH = "./db/schema.sql"

    def __init__(self, text: str) -> None:
        """
        Parameters
        ----------
        text : str
            Text that becomes a morpheme model
        """

        self.text = text

        # Morphological analysis tagger
        self.tagger = MeCab.Tagger("-Ochasen")

        self.triplet_freqs = self._make_triple_freqs()

    def _make_triple_freqs(self) -> Dict[Tuple[str, str, str], int]:
        """
        Morphological and triple occurrence frequency analysis

        Returns
        -------
        triplet_freqs : dict
            Triplets and their frequency of occurrence
        """

        sentences = self._divide(self.text)

        # Triplet and frequency dictionary
        triplet_freqs = defaultdict(int)

        for sentence in sentences:
            morphemes = self._morphological_analysis(sentence)

            # Make triplets from morpheme list
            triplets = self._make_triplet(morphemes)

            for (triplet, n) in triplets.items():
                triplet_freqs[triplet] += n

        return triplet_freqs

    def _divide(self, text: str) -> List[str]:
        """
        Split long text into one sentence according to delimiters

        Parameters
        ----------
        text : str
            Text that becomes a morpheme model

        Returns
        -------
        sentences : list of str
            Multiple sentences separated
        """

        delimiters = "。|. |\."

        # Convert all delimiters to newline characters
        text = re.sub(r"({0})".format(delimiters), r"\1\n", text)

        sentences = [sentence.strip() for sentence in text.splitlines()]

        return sentences

    def _morphological_analysis(self, sentence: str) -> List[str]:
        """
        Morphological analysis of a sentence

        Parameters
        ----------
        sentence : str
            A sentence to analyze

        Returns
        -------
        morphemes : list of str
            Morphologically divided list
        """

        morphemes = []

        node = self.tagger.parseToNode(sentence)

        while node:
            if node.posid != 0:
                morphemes.append(node.surface)
            node = node.next

        return morphemes

    def _make_triplet(self, morphemes: List[str]) -> Dict[Tuple[str, str, str], int]:
        """
        Wrap the morpheme list in triplets and measure the number of appearances

        Parameters
        ----------
        morphemes : list of str
            Morphologically divided list

        Returns
        -------
        triplet_freqs : dict
            Triplets and their frequency of occurrence
        """

        if len(morphemes) < 3:
            return {}

        # Triplet and frequency dictionary
        triplet_freqs = defaultdict(int)

        for i in range(len(morphemes) - 2):
            triplet = tuple(morphemes[i: i + 3])
            triplet_freqs[triplet] += 1

        triplet = Model.BEGIN, *morphemes[:2]
        triplet_freqs[triplet] = 1

        triplet = *morphemes[-2:], Model.END
        triplet_freqs[triplet] = 1

        return triplet_freqs

    def save(self, init: bool = False) -> None:
        """
        Save the formed model in DB

        Parameters
        ----------
        init : bool
            Flag to initialize DB
        """

        con = sqlite3.connect(Model.DB_PATH)

        if init:
            # Actually initialize the DB
            with open(Model.DB_SCHEMA_PATH, "r") as schema:
                con.executescript(schema.read())

        datas = [(*triplet, freq) for (triplet, freq) in self.triplet_freqs.items()]

        sql = "insert into triplet_freqs (prefix1, prefix2, suffix, freq) values (?, ?, ?, ?)"
        con.executemany(sql, datas)

        con.commit()
        con.close()

    def inspect(self) -> None:
        """
        Morphological model verification
        """

        triplet_freqs = self.triplet_freqs

        for triplet in triplet_freqs:
            print("|".join(triplet), triplet_freqs[triplet])
