from . import morpheme
from . import markov_c
from typing import List, TypeVar, Type, Union

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

        try:
            if not text:
                with open("./asset/" + file, encoding = "utf-8") as f:
                    text = f.read()
        except FileNotFoundError as e:
            print(NovelizerError(e))
        else:
            self.model = morpheme.Model(text)

    def build(self) -> None:
        """
        Materialize morpheme model as DB
        """

        try:
            if not self.model:
                raise ModelNotFoundError("build")
        except NovelizerError as e:
            print(e)
        else:
            self.model.save(True)

    def inspect(self) -> None:
        """
        Validate the formed morpheme model
        """

        try:
            if not self.model:
                raise ModelNotFoundError("inspect")
        except NovelizerError as e:
            print(e)
        else:
            self.model.inspect()

    def novelize(self, n: int = 1) -> List[str]:
        """
        Generate novel based on materialized morpheme model

        Parameters
        ----------
        n : int, default 1
            Number of novels to generate

        Returns
        -------
        novels : list of str
            Generated novel list
        """

        gen = markov_c.Generator(n)

        try:
            result = gen.generate()
        except FileNotFoundError as e:
            print(NovelizerError(e))
        else:
            return result


E = TypeVar("E", bound = Exception)


class NovelizerError(Exception):
    """
    Exception base for Novelizer class

    Attributes
    ----------
    name : str
        The name of the exception class
    e : class object or None
        Exception class object
    """

    def __init__(self, e: Type[Union[E, None]] = None) -> None:
        """
        Parameters
        ----------
        e : class object or None
            Exception class object
        """

        self.name = self
        self.e = e

    def __str__(self) -> str:
        """
        Returns
        -------
        err_msg : str
            An error message containing the error name and its contents
        """

        self.name = self.e
        return self.msg(str(self.e))

    @property
    def name(self) -> str:
        """
        Returns
        -------
        name : str
            The name of the exception class
        """

        return self.__name

    @name.setter
    def name(self, object) -> None:
        """
        Parameters
        ----------
        object : class object
            Exception class object
        """

        self.__name = object.__class__.__name__

    def msg(self, text: str) -> str:
        """
        Error message

        Parameters
        ----------
        text : str
            Error text

        Returns
        -------
        err_msg : str
            An error message containing the error name and its contents
        """

        return f"{ self.name }: <{ text }>"


class ModelNotFoundError(NovelizerError):
    """
    Error thrown when there is no morpheme model

    Attributes
    ----------
    type : str
        The thrown function name
    """

    def __init__(self, type: str) -> None:
        """
        Parameters
        ----------
        type : str
            The thrown function name
        """

        super().__init__()
        self.type = type

    def __str__(self) -> str:
        """
        Returns
        -------
        err_msg : str
            An error message containing the error name and its contents
        """

        return super().msg(
            f"Could not execute { self.type } function because "
            "there is no morpheme model. First, "
            "create the model using the register function.")
