from dataclasses import dataclass

from model import artObject


@dataclass
class Arco:
    o1: artObject
    o2: artObject
    peso: int