# Web Scraping - Resultados da Mega-Sena 🎱

Script Python que coleta todos os resultados históricos da Mega-Sena diretamente do site da **Caixa Econômica Federal** e armazena em formato Parquet.

## 📦 Estrutura do Projeto
```
├── buscador.py         # Script principal do web scraping
├── data/               # Pasta com resultados (gerado automaticamente)
│   └── resultados.parquet
├── pyproject.toml      # Dependências gerenciadas pelo Poetry
├── poetry.lock         # Versões exatas das dependências
└── README.md
```
## ⚙️ Pré-requisitos
Python = ">=3.12"

Poetry (gerenciador de dependências)

Conexão com internet

## 🚀 Como Usar
1. Clone o repositório:

2. Instale as dependências:

```bash
poetry install
```

3. Execute o coletor:

``` bash
poetry run python buscador.py
```

Os dados serão salvos em:

```
data/resultados.parquet
```

## Aviso Legal
Este projeto foi feito somente para fins educacionais.