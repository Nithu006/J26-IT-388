# Database decision: pending

No database, ORM, connection or migrations are implemented. See [D9](open_questions.md).
Before choosing PostgreSQL/MongoDB, establish persistence use cases, ownership,
access, retention/deletion and backups. Do not store raw text or direct identifiers
in history by default. Repository/model/db files are reserved interfaces only.
