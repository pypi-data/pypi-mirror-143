"""Helper for ViSP meta-data."""
from typing import Iterable
from typing import Union


class MetaDataMixin:
    """Class to provide meta-data helper methods."""

    def metadata_count_after_beam_split(self, tags: Union[Iterable[str], str]) -> int:
        """
        Count total number of files for a certain tag AFTER the beams have been split.

        Parameters
        ----------
        tags
            Data tags

        Returns
        -------
        int
            Number of files
        """
        number = self.scratch.count_all(tags=tags)
        if number % 2 != 0:
            raise ValueError(
                f"VISP has two beams so the total number of tagged files should be an even number. {number=}"
            )
        return (
            number // 2
        )  # Half the count as the files were split into two in the split beams task
