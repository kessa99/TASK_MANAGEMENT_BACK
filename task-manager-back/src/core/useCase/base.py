"""
Classe de base pour les Use Cases
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class UseCase(ABC, Generic[InputDTO, OutputDTO]):
    """
    Classe de base abstraite pour tous les Use Cases

    Un Use Case représente une action métier unique.
    Il prend un DTO en entrée et retourne un DTO en sortie.
    """

    @abstractmethod
    def execute(self, input_dto: InputDTO) -> OutputDTO:
        """
        Exécuter le use case

        Args:
            input_dto: Les données d'entrée

        Returns:
            Les données de sortie

        Raises:
            AppError: En cas d'erreur métier
        """
        pass
