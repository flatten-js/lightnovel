from . import morpheme

class Novelizer(object):
    """
    Generating Novels by Markov Chains Based on Morphological Models

    Attributes
    ----------
    model : morpheme.Model
        A class that forms morpheme models of Markov chains
    """

    def __init__(self) -> None:
        self.model = None

    def register(self, file: str = "title.txt", *, text: str = "") -> None:
        """
        Register the text that will be the morpheme model

        Parameters
        ----------
        file : str, default "title.txt"
            Register text from text file
        text : str, default ""
            Register text directly without going through a text file

        Notes
        -----
        Parameter priority : text < file
        """

        if not text:
            with open("./asset/" + file, encoding = "utf-8") as f:
                text = f.read()

        self.model = morpheme.Model(text)

    def build(self) -> None:
        """
        Materialize morpheme model as DB
        """

        self.model.save(True)

    def inspect(self) -> None:
        """
        Validate the formed morpheme model
        """

        self.model.inspect()
