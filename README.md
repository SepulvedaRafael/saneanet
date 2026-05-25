# 🌊 SANEANET

<a href="https://www.python.org/"><img src="https://img.shields.io/badge/PYTHON-000000?style=for-the-badge&logo=python&logoColor=3776AB" alt="HTML5"></a>
<a href="https://docs.python.org/3/library/asyncio.html"><img src="https://img.shields.io/badge/ASYNCIO-000000?style=for-the-badge&logo=python&logoColor=009688" alt="AsyncIO"></a>
<a href="https://streamlit.io/"><img src="https://img.shields.io/badge/STREAMLIT-000000?style=for-the-badge&logo=streamlit&logoColor=FF4B4B" alt="Streamlit"></a>
<a href="https://docs.astral.sh/uv/"><img src="https://img.shields.io/badge/UV-000000?style=for-the-badge&logo=uv&logoColor=#DE5FE9" alt="UV"></a>
<a href="https://socket.io/"><img src="https://img.shields.io/badge/SOCKETS-000000?style=for-the-badge&logo=socketdotio&logoColor=010101" alt="Sockets"></a>

Esse projeto foi desenvolvido como parte das Atividades Práticas Supervisionadas (APS) do curso de Ciência da Computação (CC) da Universidade Paulista, visando criar uma aplicação para que inspetores de indústras do meio ambiente compartilhem dados com a Secretaria de Estado do Meio Ambiente por meio da utilização do conceito de Sockets de Berkeley.

Nesse sentido, o SANEANET é uma ferramenta de comunicação ambiental via sockets desenvolvida em Python, projetada para permitir o monitoramento em tempo real das atividades industriais que impactam o Rio Tietê. A solução utiliza o protocolo TCP/IP para garantir entrega confiável de dados entre inspetores de campo e a Secretaria de Estado do Meio Ambiente.

> [!NOTE]
> 🎯 Objetivo: Minimizar o tempo de resposta das autoridades ambientais e impedir que resíduos tóxicos causem danos ao rio e à saúde da população, através de uma comunicação direta, estável e concorrente.

## 💻 Pré-requisitos
Antes de iniciar, certifique-se de possuir:

- Python 3.13 instalado (versão estável recomendada)
- Git instalado e configurado
- Gerenciador de dependências: uv instalado
- Ambiente de desenvolvimento (VS Code, PyCharm, etc)
- Acesso de administrador para configuração do firewall
- Conexão de rede funcional entre cliente e servidor

## 🚀 Instalando as dependências
Para instalar o uv que é utiliza:

```bash
# Linux/MacOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Em seguida, vá para a pasta que deseja clonar esse repositório e digite:
```bash
git clone https://github.com/SepulvedaRafael/saneanet.git
cd saneanet
```

Após a clonagem, execute cada um dos comandos abaixo:
```bash
# Criar ambiente virtual
uv venv

# Ativar ambiente virtual
# WINDOWS
.venv\Scripts\activate

# LINUX/MAC
source .venv/bin/activate

# Instalar e sincronizar dependências
uv pip install -r pyproject.toml
uv sync
```

## 🔐 Configuração de Firewall
> [!WARNING]
> Atenção: O SANEANET utiliza a porta TCP 9999 para comunicação entre cliente e servidor. Sem a configuração adequada do firewall, as conexões serão bloqueadas e o sistema não funcionará corretamente.

### 🔷 Windows
#### Opção 1: Via PowerShell (Administrador)
```bash
# Liberar porta 9999 para entrada TCP
New-NetFirewallRule -DisplayName "SANEANET Server" -Direction Inbound -LocalPort 9999 -Protocol TCP -Action Allow

# (Opcional) Liberar para saída também
New-NetFirewallRule -DisplayName "SANEANET Client" -Direction Outbound -LocalPort 9999 -Protocol TCP -Action Allow
```

#### Opção 2: Via Prompt de Comando (Administrador)
```bash
netsh advfirewall firewall add rule name="SANEANET Server" dir=in action=allow protocol=TCP localport=9999
```

#### Opção 3: Interface Gráfica

1. Abra **Painel de Controle > Firewall do Windows**
2. Clique em **Configurações Avançadas**
3. Em **Regras de Entrada > Nova Regra**
4. Selecione **Porta > TCP >** Porta específica: 9999
5. Marque **Permitir a conexão**
6. Aplique para todos os perfis (Domínio, Privado e Público)
7. Nomeie a regra como preferir.

### 🔶 Linux
#### Ubuntu/Debian (UFW)
```bash
# Liberar porta 9999 TCP
sudo ufw allow 9999/tcp

# Recarregar regras
sudo ufw reload

# Verificar status
sudo ufw status
```

## 💻 Executando o Projeto

### 1. Iniciando o Servidor Central (Secretaria)

O servidor deve ser executado primeiro, pois aguarda conexões dos clientes:

```bash
# Com o ambiente virtual ativado e sincronizado
uv run server/server.py
```

✅ Saída esperada:

```bash
============================================================
 SANEANET- Servidor da Secretaria 🌊
  Escutando em 0.0.0.0:9999
============================================================
```

### 2. Iniciando o Dashboard de Monitoramento

Em um **novo terminal** ainda no computador do servidor, execute o painel da Secretaria:

```bash
uv run streamlit run server/dashboard.py --server.port 8503
```

🌐 O dashboard será aberto automaticamente em http://localhost:8503

### 3. Iniciando o Terminal do Inspetor (Cliente)

Em outro computador, abra um terminal e execute a interface do inspetor:

```bash
uv run streamlit run client/app.py --server.port 8501
```

🌐 A interface do inspetor será aberta em http://localhost:8501

## 📡 Configurando a Conexão Cliente-Servidor

Na interface do inspetor (app.py), configure os parâmetros de conexão na barra lateral:

| Parâmetro | Valor Padrão | Descrição |
| --- | --- | --- |
| IP do servidor  | 127.0.0.1 | Endereço IP do servidor (Use o IP real da rede para conexão remota)
| Porta  | 9999 | Porta TCP da escuta do servidor
| ID do Inspetor  | INS-001 | Identificador único do inspetor
| Indústria  | Selecionável | Planta industrial onde o inspetor está alocado
| Turno  | Manhã/Tarde/Noite | Período de atuação da equipe

> [!IMPORTANT]
> Para comunicação em rede real (não localhost), substitua 127.0.0.1 pelo IP público ou interno do servidor e certifique-se de que a porta 9999 esteja liberada no firewall do servidor e em qualquer roteador intermediário.

## 📦 Estrutura do Projeto

```bash
saneanet/
├── shared/
│   └── protocol.py        # Protocolo compartilhado: serialização JSON, delimitadores
├── client/
│   └── app.py             # Interface do Inspetor (Streamlit)
├── server/
│   ├── server.py          # Servidor central assíncrono (asyncio + sockets)
│   ├── dashboard.py       # Painel de monitoramento da Secretaria (Streamlit)
│   └── data/              # Diretório de persistência (gerado automaticamente)
│       ├── messages.json  # Relatórios recebidos
│       └── files/         # Arquivos de evidência (PDFs, imagens)
├── pyproject.toml         # Dependências e configuração do projeto
├── uv.lock               # Lockfile de dependências
└── README.md             # Este arquivo
```

## 🧪 Testando a Comunicação

1. Inicie o **servidor** e verifique se está escutando na porta 9999
2. Inicie o **dashboard** para visualizar os relatórios em tempo real
3. Inicie o **cliente** e preencha os dados de conexão
4. Envie uma **mensagem de texto** com nível de urgência
5. Envie uma **arquivo de envidência** (PDF ou imagem)
6. Verifique no dashboard se os dados foram recebidos corretamente

### Comandos úteis para diagnóstico

```bash
# Verificar se a porta 9999 está em escuta
# Windows
netstat -ano | findstr :9999

# Linux
ss -tlnp | grep 9999
# ou
netstat -tlnp | grep 9999

# Testar conectividade com o servidor
# Windows
Test-NetConnection -ComputerName <IP_SERVIDOR> -Port 9999

# Linux
nc -zv <IP_SERVIDOR> 9999
# ou
telnet <IP_SERVIDOR> 9999
```

## ⚙️ Funcionalidades Implementadas

| Funcionalidade | Descrição |
| --- | --- |
| 📤 Envio de mensagens | Texto estruturado com metadados (inspetor, indústria, urgência) |
| 📎 Transferência de arquivos | Envio de PDFs e imagens como evidência ambiental |
| 🎨 Interface gráfica | Streamlit para usabilidade simplificada em campo e na central |
| ⚡ Concorrência assíncrona | asyncio para suportar múltiplos inspetores simultâneos |
| 🔒 Confiabilidade TCP | Garantia de entrega ordenada e sem perdas de dados |
| 🗂️ Persistência local | Armazenamento de relatórios em JSON e arquivos em disco |
| 🚦 Categorização visual | Cores (verde/amarelo/vermelho) para triagem rápida de urgência |

Caso queira fazer algumas requisições para saber se os endpoints estão funcionando, fique a vontade para executar o comando acima e ir na pasta `requests`. Certifique-se de ter a extensão REST Client (VScode ou Cursor) instalado e clique siga a ordem: POST, GET, PUT e DELETE. Para executar cada um desses arquivos, basta clicar em `Send request`.

## 🛠️ Ferramentas de Qualidade de Código

O projeto utiliza ferramentas modernas para garantir manutenibilidade:

| Ferramenta | Finalidade |
| --- | --- |
| 🐦 Ruff | Linting e formatação automática (PEP 8) |
| 🧪 Mypy | Verificação estática de tipos (type hints) |
| 🔄 uv | Gerenciamento rápido de dependências e ambientes virtuais |
| 📦 Git + GitHub | Controle de versão e colaboração em equipe |

### Executando verificações de qualidade

```bash
# Formatar código com Ruff
ruff format .

# Analisar código com Ruff
ruff check .

# Verificar tipos com Mypy
mypy .
```

## 🚨 Solução de Problemas Comuns

| Problema | Possível Causa | Provável Solução | 
| --- | --- | --- |
| ❌ "Connection refused"| Firewall bloqueando porta 9999 | Configure as regras de firewall conforme seção acima
| ❌ Servidor não inicia | Porta 9999 já em uso | Use netstat para identificar o processo e libere a porta
| ❌ Cliente não conecta | IP do servidor incorreto | Verifique se está usando o IP correto da rede
| ❌ Arquivos não salvos | Permissão de escrita no diretório | Execute com privilégios adequados ou ajuste permissões
| ❌ Mensagens "grudadas" | Delimitador não processado | Verifique se o protocol.py está sendo importado corretamente

## 📚 Referências Técnicas

- **Modelo TCP/IP:** Garantia de entrega confiável via Three-Way Handshake
- **Sockets de Berkeley:** API padrão para comunicação em rede
- **AsyncIO:** Gerenciamento assíncrono de múltiplas conexões
- **JSON + UTF-8:** Serialização flexível e compatível com caracteres especiais
- **Streamlit:** Framework para interfaces web em Python puro

> [!NOTE]
> Futuras Melhorias: Este projeto foi desenvolvido como prova de conceito acadêmica. Para implantação em produção, recomenda-se:
> - 🔐 Implementar criptografia TLS/SSL para proteger dados sensíveis
> - 🔑 Adicionar autenticação e autorização de usuários
> - 🗄️ Migrar persistência para banco de dados relacional
> - 📊 Implementar logs estruturados e monitoramento de saúde do sistema
> - 🌐 Adicionar suporte a reconexão automática em caso de falha de rede

---

**Desenvolvido por:** Júlia dos Santos Martins, Lucas Alexsandre Aguiar Martins e Rafael Arley de Sousa Sepulveda  
**Instituição:** UNIP – Universidade Paulista, Faculdade de Ciência da Computação  
**Ano:** 2026 🌊🐟🌿
