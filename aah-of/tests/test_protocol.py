import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# test_term_protocol.py

from app.domain.interfaces.TermServiceProtocol import TermServiceProtocol
from app.infrastructure.repositories.term_repository_impl import TermRepositoryImpl
from sqlmodel import create_engine, Session

import pytest

# Crée un faux moteur SQLite pour le test
engine = create_engine("sqlite://", echo=False)

class A:
    pass

def test_repository_respects_protocol():
    with Session(engine) as session:
        repo = TermRepositoryImpl(session)
        assert isinstance(repo, TermServiceProtocol), "TermRepositoryImpl does not match TermServiceProtocol"
