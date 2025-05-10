import sqlite3
import threading

from trackJobs.exceptions import InicializacaoBancoException


class BancoDeDados:
    _instancia = None
    _lock = threading.Lock()

    def __new__(cls, db_path="track_jobs.db"):
        with cls._lock:
            if cls._instancia is None:
                cls._instancia = super(BancoDeDados, cls).__new__(cls)
                cls._instancia._initialized = False
        return cls._instancia

    def __init__(self, db_path="track_jobs.db"):
        if not self._initialized:
            self.db_path = db_path
            self.conexao = sqlite3.connect(self.db_path)
            self.cursor = self.conexao.cursor()
            self._initialized = True

    def close_conexao(self):
        if self.conexao:
            self.conexao.close()
            self._initialized = False
            self._instancia = None

    def inicializa_banco(self):
        try:
            self.cursor.execute(
                """create table if not exists empresas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                site TEXT,
                setor TEXT
                )"""
            )

            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS vagas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                link TEXT NOT NULL UNIQUE,
                status TEXT DEFAULT 'candidatar-se'
                CHECK(status IN
                ('candidatar-se', 'em análise', 'entrevista', 'rejeitado', 'aceito')),
                data_aplicaçao DATE,
                descriçao TEXT,
                idEmpresa INTEGER,
                FOREIGN KEY(idEmpresa) REFERENCES empresas(id)
                )"""
            )
        except Exception as e:
            raise InicializacaoBancoException(
                "Erro ao inicializar o banco de dados"
            ) from e
