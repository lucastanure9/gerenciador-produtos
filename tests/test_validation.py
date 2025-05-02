# test_validation.py

import pytest
from application.domain.validation import validar_int, validar_nome, validar_preco, validar_data


def test_validar_int_valido():
    assert validar_int("123") == 123


def test_validar_int_invalido():
    assert validar_int("abc") is None
    assert validar_int("") is None


def test_validar_nome_valido():
    assert validar_nome("Produto") == "Produto"
    assert validar_nome("  Produto  ") == "Produto"


def test_validar_nome_vazio():
    assert validar_nome("") is None
    assert validar_nome("   ") is None


def test_validar_preco_com_ponto():
    assert validar_preco("10.50") == 10.50


def test_validar_preco_com_virgula():
    assert validar_preco("10,50") == 10.50


def test_validar_preco_invalido():
    assert validar_preco("abc") is None
    assert validar_preco("-5") is None
    assert validar_preco("") is None


def test_validar_data_valida():
    assert validar_data("01-01-2024") == "01-01-2024"


def test_validar_data_com_barra():
    assert validar_data("01/01/2024") == "01-01-2024"


def test_validar_data_invalida():
    assert validar_data("31-02-2024") is None
    assert validar_data("2024-01-01") is None
    assert validar_data("") is None
