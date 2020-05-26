import random
import os.path
import sqlite3
from . import morpheme
from typing import List, Dict, Tuple

class Generator(object):
    """
    Generate sentences using Markov chain based on morpheme model
    """

    def __init__(self, n: int) -> None:
        """
        Parameters
        ----------
        n : int
            Number of sentences to generate
        """

        self.n = n
        self.con = None

    def _connector(self) -> "sqlite3.Connection":
        """
        Secure connection with DB

        Returns
        -------
        con : sqlite3.Connection
            sqlite3 connection object
        """

        path = morpheme.Model.DB_PATH

        if not os.path.exists(path):
            raise FileNotFoundError(f"No such DB file: '{ path }'")

        con = sqlite3.connect(morpheme.Model.DB_PATH)

        # Make query results accessible by column name
        con.row_factory = sqlite3.Row

        return con


    def generate(self) -> List[str]:
        """
        Actually produces the specified number of sentences

        Returns
        -------
        sentences : list of str
            List of specified number of sentences
        """

        self.con = self._connector()

        sentences = [self._generate_sentence() for _ in range(self.n)]

        self.con.close()

        return sentences

    def _generate_sentence(self) -> str:
        """
        Generate one sentence at random

        Returns
        -------
        generated_text : str
            Randomly generated sentences
        """

        morphemes = []

        first_triplet = self._get_first_triplet()
        morphemes.extend(first_triplet[1:])

        while morphemes[-1] != morpheme.Model.END:
            prefixes = tuple(morphemes[-2:])
            triplet = self._get_triplet(prefixes)
            morphemes.append(triplet[-1])

        return "".join(morphemes[:-1])

    def _fetch_model(self, prefixes: Tuple[str, ...]) -> List[dict]:
        """
        Fetch morpheme model from DB

        Parameters
        ----------
        prefixes : tuple
            Some prefixes that are search conditions

        Returns
        -------
        model : list of dict
            Morphological model
        """

        sql = "select prefix1, prefix2, suffix, freq from triplet_freqs where prefix1 = ?"

        if (len(prefixes)) == 2:
            sql += " and prefix2 = ?"

        cursor = self.con.execute(sql, prefixes)

        return [dict(row) for row in cursor]

    def _get_triplet(self, prefixes: Tuple[str, ...]) -> Tuple[str, str, str]:
        """
        Get triplet randomly based on prefixes

        Parameters
        ----------
        prefixes : tuple
            Acquisition condition

        Returns
        -------
        triplet : tuple
            Randomly acquired triplet
        """

        model = self._fetch_model(prefixes)

        return self._get_probably_triplet(model)

    def _get_first_triplet(self) -> Tuple[str, str, str]:
        """
        Randomly obtain the triplet of the beginning of a sentence

        Returns
        -------
        triplet : tuple
            Triplet of sentence heads randomly acquired
        """

        prefixes = morpheme.Model.BEGIN,

        return self._get_triplet(prefixes)

    def _get_probably_triplet(self, model: List[dict]) -> Tuple[str, str, str]:
        """
        Probabilistically select triplet from the model

        Parameters
        ----------
        model : list of dict
            Morphological model

        Returns
        -------
        triplet : tuple
            Probabilistically selected triplet
        """

        probablity = []

        for (index, triplet_freqs) in enumerate(model):
            for _ in range(triplet_freqs.pop("freq")):
                probablity.append(index)

        model_index = random.choice(probablity)

        return tuple(model[model_index].values())
