# 💰 FINGEST - Aplicação de Gestão Financeira Simplificada

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Kivy](https://img.shields.io/badge/Kivy-2.1.0-green?logo=kivy)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite)
![Licença](https://img.shields.io/badge/Licença-MIT-yellow)

## 📌 Visão Geral

**FINGEST** é uma aplicação desktop desenvolvida no âmbito do curso do **IPPLS** para responder a um problema real: a dificuldade que muitas pessoas sentem em gerir o seu dinheiro devido à complexidade das aplicações financeiras, linguagem técnica e excesso de informações.

O nosso objetivo é oferecer uma ferramenta **simples, clara e acessível**, especialmente pensada para utilizadores com **baixa literacia financeira** e/ou **dificuldades visuais**, permitindo um acompanhamento eficaz de despesas, receitas e poupanças.

---

## 🎯 Público-alvo

- Pessoas com pouca experiência em gestão financeira.
- Utilizadores que necessitam de interfaces limpas e de fácil compreensão.
- Pessoas com dificuldades visuais (suporte a contraste elevado e fontes ajustáveis).

---

## ✨ Funcionalidades Principais

- **Registo de Transações**: Adicione, edite e elimine despesas e receitas de forma intuitiva.
- **Visão Geral do Saldo**: Acompanhe o saldo atualizado em tempo real.
- **Metas de Poupança**: Defina objetivos financeiros e monitore o progresso.
- **Categorização**: Organize os gastos por categorias (alimentação, lazer, transporte, etc.).
- **Filtros e Pesquisa**: Consulte o histórico por data ou tipo de transação.
- **Exportação de Dados**: (Em desenvolvimento) Exporte relatórios para CSV/PDF.

### ♿ Funcionalidades de Acessibilidade
- **Alto Contraste**: Interface otimizada para utilizadores com baixa visão.
- **Fontes Redimensionáveis**: Ajuste o tamanho do texto conforme a necessidade.
- **Navegação por Teclado**: Possibilidade de utilizar a aplicação apenas com o teclado (Tab, Enter, Setas).
- **Interface Limpa**: Sem poluição visual ou jargões financeiros complexos.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** – Linguagem de programação principal.
- **Kivy** – Framework para desenvolvimento da interface gráfica (GUI) multiplataforma.
- **SQLite3** – Base de dados local leve e eficiente para armazenamento das informações.
- **VS Code** – Ambiente de desenvolvimento integrado (IDE) utilizado.

---

## 📂 Estrutura do Projeto

A organização dos ficheiros é simples e modular, facilitando a manutenção e expansão:
```
fingest/ # Pasta raiz do projeto
├── main.py # Ponto de entrada da aplicação (inicia o ciclo Kivy)
├── database.py # Gerencia a conexão e operações CRUD com SQLite
├── fingest.kv # Ficheiro principal de layout Kivy (estilos e estrutura visual)
└── screens/ # Módulo com as diferentes telas da aplicação
├── init.py # Torna o diretório um pacote Python
├── dashboard.py # Tela com visão geral do saldo e resumo
├── transacoes.py # Tela para registo, edição e listagem de despesas/receitas
├── poupancas.py # Tela para definir e monitorizar metas de poupança
└── config.py # Tela de configurações (tema, tamanho de fonte, etc.)
```

# Autor

**Académico:** Onésimo Supe

**Curso:** Gestão de Redes e Sistemas Informáticos

**Instituição:** Instituto Politécnico Privado Lucrécio dos Santos (IPPLS)

**Ano:** 2026
