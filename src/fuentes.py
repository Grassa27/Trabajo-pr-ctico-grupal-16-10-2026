"""Fuentes de datos: interfaz común y lectores CSV y JSON."""
import csv
import json
from abc import ABC, abstractmethod


class FuenteDatos(ABC):
    @abstractmethod
    def cargar(self, ruta):
        """Devuelve una lista de diccionarios."""


class FuenteCSV(FuenteDatos):
    def cargar(self, ruta):
        with open(ruta, encoding="utf-8", newline="") as archivo:
            return list(csv.DictReader(archivo))


class FuenteJSON(FuenteDatos):
    def cargar(self, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, list):
            raise ValueError(f"El JSON debe contener una lista de registros, se obtuvo {type(datos).__name__}")
        return datos
