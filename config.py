# config.py: provides MySQL conenction settings used by repository layer
# placed alongside app.py in project root
# Connection values are read from environment variables so credentialsare not stored in the repository.
import os
config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "grammar_db"),
    "charset": "utf8mb4"
}
