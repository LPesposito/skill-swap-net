# Skill Swap (SkillSwapProject)

Projeto Django mínimo para uma plataforma de troca de habilidades (Skill Swap). Este repositório contém o projeto `SkillSwapProject` e apps que implementam usuários, serviços (ofertas/solicitações) e comunicação (chat).

## Estrutura principal

- `SkillSwapProject/` — pacote do projeto Django (settings, asgi, urls, wsgi)
- `core/` — app core (esqueleto)
- `users/` — perfis de usuário, habilidades e view de perfil
- `services/` — solicitações de serviço e avaliações (reviews)
- `communication/` — modelos de chat e consumers do Channels
- `.venv/` — ambiente virtual local (não comitado normalmente)

## Tecnologias

- Python 3.13
- Django 5.2.8
- Django Channels 4 (suporte a WebSockets)
- ASGI server recomendado: Daphne ou Uvicorn

Consulte `requirements.txt` para as versões instaladas no ambiente virtual usado aqui.

## Setup local (Windows / PowerShell)

1. Criar e ativar o ambiente virtual (se ainda não existir):

```powershell
# Criar ambiente
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt

# Ativar (PowerShell)
.venv\Scripts\Activate.ps1
```

2. (Opcional) Variáveis de ambiente para PostgreSQL:

```powershell
$env:POSTGRES_DB = "skillswap"
$env:POSTGRES_USER = "postgres"
$env:POSTGRES_PASSWORD = "postgres"
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_PORT = "5432"
```

3. Rodar migrações e criar um superuser:

```powershell
.venv\Scripts\python .\SkillSwapProject\manage.py migrate
.venv\Scripts\python .\SkillSwapProject\manage.py createsuperuser
```

4. Rodar o servidor de desenvolvimento (HTTP):

```powershell
.venv\Scripts\python .\SkillSwapProject\manage.py runserver
```

### Testar WebSockets (ASGI)

Para testar WebSockets via Channels é necessário rodar um servidor ASGI como Daphne ou Uvicorn.

Exemplos (instale daphne ou uvicorn se necessário):

```powershell
# usando daphne
.venv\Scripts\python -m pip install daphne
.venv\Scripts\daphne -b 127.0.0.1 -p 8001 SkillSwapProject.asgi:application

# usando uvicorn
.venv\Scripts\python -m pip install uvicorn
.venv\Scripts\python -m uvicorn SkillSwapProject.asgi:application --host 127.0.0.1 --port 8001
```

Endpoint WebSocket de exemplo: `ws://127.0.0.1:8001/ws/chat/<room_name>/`

## Funcionalidades implementadas (estado atual)

- Apps criados: `core`, `users`, `services`, `communication`
- Models implementados:
  - `users.UserSkill`, `users.UserProfile`
  - `services.ServiceRequest`, `services.Review`
  - `communication.ChatRoom`, `communication.ChatMessage`
- URLs principais:
  - `accounts/` (autenticação Django), `users/` e `services/` incluídos no `urls.py` do projeto
  - `users` possui a rota `profile/<username>/` com template
- Channels:
  - Layer in-memory configurada para desenvolvimento
  - `communication.ChatConsumer` implementado (WebsocketConsumer básico)
  - WebSocket routing em `communication/routing.py`

## Observações importantes

- O channel layer in-memory é adequado apenas para desenvolvimento/local; para produção use Redis (`channels_redis`).
- `requirements.txt` contém os pacotes instalados no venv atual; ajuste conforme necessário para produção.

## Próximos passos sugeridos

- Registrar modelos no admin para gestão via painel administrativo.
- Adicionar testes unitários para models, views e consumers.
- Configurar `channels_redis` com Redis para ambientes de staging/production.
- Expandir `UserSkill` para diferenciar oferta e procura, se o domínio exigir.

---

Se desejar, posso também:

- Adicionar `daphne` e `uvicorn` ao `requirements.txt` e instalá-los no venv.
- Gerar um `requirements-dev.txt` com ferramentas de desenvolvimento.
- Inicializar um repositório Git e criar um commit inicial com as alterações.

## Proposta do projeto

Proposta: 💡 SkillSwap: Plataforma de Troca de Habilidades

O SkillSwap é um projeto de marketplace colaborativo desenvolvido como Projeto Integrador (PI) para facilitar a troca de conhecimento e serviços entre usuários. Nossa plataforma conecta pessoas que buscam aprender uma nova habilidade ou necessitam de um serviço ("Estou buscando ajuda com jardinagem") com aquelas que oferecem seu tempo e expertise ("Eu ensino Python").

Recursos Principais
- Perfis Detalhados: Cadastro de perfis com mapeamento de habilidades oferecidas e solicitadas.
- Sistema de Matching: Lógica de busca e oferta/pedido para conectar usuários com interesses compatíveis.
- Comunicação Integrada: Chat simples em tempo real para negociação e acompanhamento dos serviços.
- Reputação Baseada em Avaliações: Sistema de avaliação 1-5 estrelas para construir a confiança da comunidade após a conclusão de uma troca.

Stack de Tecnologia
- Backend: Python com Django (Framework robusto e seguro).
- Banco de Dados: PostgreSQL (Para escalabilidade e complexidade de dados).
- Comunicação em Tempo Real: Django Channels (Utilizando WebSockets para o chat).

## Conformidade do repositório com a proposta

Abaixo segue um mapeamento rápido do que já está implementado neste scaffold e o que falta para cumprir completamente a proposta do SkillSwap.

- Perfis Detalhados: PARCIAL
  - Implementado: `UserProfile` (1:1 com User) e `UserSkill` (habilidades associadas ao usuário).
  - Falta/Próximo: formular campos adicionais (nível, tags, oferta vs demanda), endpoints de edição/CRUD públicos e importação/exportação de skills.

- Sistema de Matching: NÃO IMPLEMENTADO
  - Observação: o modelo de domínio (UserSkill, ServiceRequest) está presente e permite construir um motor de matching; porém não existe ainda lógica de busca/algoritmo de correspondência.

- Comunicação Integrada: PARCIAL
  - Implementado: modelos `ChatRoom` e `ChatMessage`, `ChatConsumer` (WebsocketConsumer) e roteamento ASGI com Channels.
  - Observação: usa um channel layer in-memory para desenvolvimento. Para produção/rede multi-processo é necessário configurar `channels_redis` com Redis e possivelmente autenticação/permissions adicionais no consumer.

- Reputação Baseada em Avaliações: PARCIAL
  - Implementado: modelo `Review` ligado a `ServiceRequest` (OneToOne) e método `get_average_rating` anexado ao User para calcular média de avaliação.
  - Observação: fluxo completo (por exemplo, criação automática da review após marcação de serviço como concluído, UI para avaliar, e exposição pública da reputação) ainda precisa ser implementado.

## Conclusão e próximos passos para cumprir 100% da proposta

Este repositório já fornece a maior parte da modelagem e infraestrutura necessária para construir o SkillSwap (modelos de perfil, skills, pedidos de serviço, avaliações e chat em tempo real). Os próximos passos principais para alinhar totalmente ao escopo da proposta são:

1. Implementar o sistema de matching (algoritmo de busca/compatibilidade e endpoints de busca).
2. Completar as UIs/CRUDs para gerenciar perfis, skills, ofertas e solicitações.
3. Implementar fluxos de transação (criar ServiceRequest, aceitar provider, marcar conclusão, criar Review automaticamente).
4. Configurar um channel layer persistente (Redis) para chat em produção e adicionar testes/segurança ao consumer.
5. Migrar para PostgreSQL para ambientes de produção e testes avançados (atualmente o projeto usa SQLite por padrão, com instruções prontas para Postgres no `settings.py`).

Se desejar, posso começar implementando os itens 1 e 3 (matching e fluxos de transação), ou criar endpoints e telas básicas para administrar perfis e skills. Diga qual prioridade você prefere e eu sigo implementando.

## Dados de demonstração (comando seed_demo)

Para facilitar testes e demonstrações, existe um comando management que popula o banco com dados de exemplo:

```powershell
.venv\Scripts\python .\SkillSwapProject\manage.py seed_demo
```

O que o comando cria (resumo):

- Usuários: `alice`, `bob`, `carol` (senha padrão para todos: `password`).
- `UserProfile` para cada usuário (bio e location de exemplo).
- `UserSkill` de exemplo: Alice (Python), Bob (Jardinagem), Carol (Design).
- `ServiceRequest` de exemplo (bob -> alice) marcado como COMPLETED e com `Review` 5 estrelas criado; outro pedido (alice -> carol) em PENDING.
- `ChatRoom` entre Alice e Bob com algumas mensagens exemplo.

O comando usa `get_or_create` para evitar duplicatas em re-execuções e é seguro para usar em um banco de desenvolvimento local.

Dica: após rodar o comando, você pode efetuar login com `alice`/`password` e navegar em `/users/skills/`, `/users/profile/alice/` e no admin para visualizar os dados inseridos.


## Como visualizar o projeto localmente (passo a passo rápido)

Após seguir o passo de setup (criar/ativar venv e instalar as dependências em `requirements.txt`), estes passos rápidos mostram como deixar a aplicação funcionando e visualizar as páginas e UIs adicionadas:

1. Rode as migrações e crie um superuser (apenas na primeira vez):

```powershell
.venv\Scripts\python .\SkillSwapProject\manage.py migrate
.venv\Scripts\python .\SkillSwapProject\manage.py createsuperuser
```

2. Inicie o servidor de desenvolvimento HTTP (padrão Django):

```powershell
.venv\Scripts\python .\SkillSwapProject\manage.py runserver
```

3. Abra o navegador e acesse as páginas para visualizar as UIs básicas:

- Admin (criar usuários/perfis/skills manualmente): http://127.0.0.1:8000/admin/
- Lista de skills (usuário logado): http://127.0.0.1:8000/users/skills/
- Adicionar skill: http://127.0.0.1:8000/users/skills/add/
- Editar perfil (usuário logado): http://127.0.0.1:8000/users/profile/<username>/edit/
- Visualizar perfil público: http://127.0.0.1:8000/users/profile/<username>/

Observação: para testar as páginas de usuário (lista de skills, editar perfil) você precisa estar logado. Use `/accounts/login/` (rota padrão do Django auth) para efetuar login.

Se preferir testar o chat via WebSocket, rode um servidor ASGI (Daphne/uvicorn) conforme instruções já presentes neste README e conecte-se ao endpoint:

`ws://127.0.0.1:8001/ws/chat/<room_name>/`

