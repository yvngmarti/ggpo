- GGPO

  - alembic
    - versions (carpeta con todas las versiones)
    - env.py
  - app
    - api
      - helpers
        - **init**.py
        - api_response.py
        - auth_dependencies.py
        - dependencies.py
      - repositories
        - bank_account_repository.py
        - expense_repository.py
        - expense_status_repository.py
        - payment_status_repository.py
        - project_repository.py
        - provider_repository.py
        - role_repository.py
        - transaction_type_repository.py
        - user_repository.py
      - routers
        - auth.py
        - bank_accounts.py
        - expense_statements.py
        - expenses.py
        - payment_statements.py
        - projects.py
        - providers.py
        - roles.py
        - transaction_types.py
        - users.py
      - schemas
        - auth_schema.py
        - bank_account_schema.py
        - expense_schema.py
        - expense_status_schema.py
        - payment_status_schema.py
        - project_schema.py
        - provider_schema.py
        - role_schema.py
        - transaction_type_schema.py
        - user_schema.py
      - services
        - **init**.py
        - auth_service.py
        - bank_account_service.py
        - expense_service.py
        - expense_status_service.py
        - payment_status_service.py
        - project_service.py
        - provider_service.py
        - role_service.py
        - transaction_type_service.py
        - user_service.py
    - core
      - database
        - **init**.py
        - base.py
        - db.py
        - session.py
      - config.py
      - security.py
    - models
      - **init**.py
      - catalogs.py
      - operational.py
    - seeds
      - **init**.py
      - initial_data.py
      - seed_data.py
    - utils
      - **init**.py
      - constants.py
      - mixins.py
    - main.py
  - diagrams
    - class_diagram.jpg
    - database_diagram_3nf.png
    - flow_diagram.jpg
    - general_use_case.jpg
  - scripts
    - seed_db.py
  - .env.template
  - .gitignore
  - alembic.ini
  - docker-compose.yml
  - requirements.txt

- env.py:

- **init**.py (de la carpeta helpers):
- api_response.py:
- auth_dependencies.py:
- dependencies.py:

- bank_account_repository.py:
- expense_repository.py:
- expense_status_repository.py:
- payment_status_repository.py:
- project_repository.py:
- provider_repository.py:
- role_repository.py:
- transaction_type_repository.py:
- user_repository.py:

- auth.py:
- bank_accounts.py:
- expense_statements.py:
- expenses.py:
- payment_statements.py:
- projects.py:
- providers.py:
- roles.py:
- transaction_types.py:
- users.py:

- auth_schema.py:
- bank_account_schema.py:
- expense_schema.py:
- expense_status_schema.py:
- payment_status_schema.py:
- project_schema.py:
- provider_schema.py:
- role_schema.py:
- transaction_type_schema.py:
- user_schema.py:

- **init**.py (de la carpeta services):
- auth_service.py:
- bank_account_service.py:
- expense_service.py:
- expense_status_service.py:
- payment_status_service.py:
- project_service.py:
- provider_service.py:
- role_service.py:
- transaction_type_service.py:
- user_service.py:

- **init**.py (de la carpeta database):
- base.py:
- db.py:
- session.py:
- config.py:
- security.py:

- **init**.py (de la carpeta models):
- catalogs.py:
- operational.py:

- **init**.py (de la carpeta seeds):
- initial_data.py:
- seed_data.py:

- **init**.py (de la carpeta utils):
- constants.py:
- mixins.py:
- main.py:

- class_diagram.jpg:
- database_diagram_3nf.png:
- flow_diagram.jpg:
- general_use_case.jpg:

- seed_db.py:
- .env.template:
- .gitignore:
- alembic.ini:
- docker-compose.yml:
- requirements.txt:

delete from public.roles;
delete from public.transaction_types tt;
delete from public.payment_status ps;
delete from public.expense_status es;
delete from public.projects p;
delete from public.bank_accounts ba;
delete from public.providers p;
delete from public.users u;
