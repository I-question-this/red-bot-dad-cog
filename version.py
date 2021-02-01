
class Version:
    def __init__(self, major:int, minor:int, bug:int):
        """Object for version recording.
        Uses the major.minor.bug notation.

        Parameters
        ----------
        major: int
            The major number for the version number.
        minor: int
            The minor number for the version number.
        bug: int
            The bug number for the version number.
        """
        self.major = major
        self.minor = minor
        self.bug = bug


    def __str__(self) -> str:
        """Turn this object into a nicely formatted string"""
        return f"{self.major}.{self.minor}.{self.bug}"


    def __eq__(self, other:"Version") -> bool:
        """Perform an equality check between this and another Version object

        Parameters
        ----------
        other: Version
            Another version object to check equality of.

        Returns
        bool
            Rather the two Version objects are equal.
        """
        if self.major != other.major:
            return False
        elif self.minor != other.minor:
            return False
        elif self.bug != other.bug:
            return False
        else:
            return True


    @staticmethod
    def from_str(string:str) -> "Version":
        """Turn a string of numbers into a Version object

        Parameters
        ----------
        string: str
            The format is major.minor.bug, and they should be
            integers

        Returns
        -------
        Version
            The constructed Version object.
        """
        if string is None:
            return Version(0,0,0)
        else:
            numbers = string.split(".")
            return Version(
                int(numbers[0]),
                int(numbers[1]),
                int(numbers[2])
                )


# The version for DadBot
__version__ = Version(1,0,0)

