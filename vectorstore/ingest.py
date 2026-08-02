import chromadb

client = chromadb.PersistentClient(path="vectorstore/chroma_data")

collection = client.get_or_create_collection(name="autodev_knowledge")

KNOWLEDGE_BASE = [
    {
        "id": "fastapi_structure_1",
        "category": "backend",
        "text": (
            "FastAPI best practice: organize routes using APIRouter, keep business logic "
            "in separate service classes rather than inside route handlers. Use Pydantic "
            "models for request and response validation. Always use dependency injection "
            "(Depends) for database sessions and authentication instead of global variables."
        ),
    },
    {
        "id": "fastapi_security_1",
        "category": "backend",
        "text": (
            "FastAPI security best practice: never store plaintext passwords. Always hash "
            "passwords with bcrypt via passlib before saving to the database. Use JWT tokens "
            "for stateless authentication, and validate tokens on every protected route using "
            "a dependency function. Never expose password hashes in API responses."
        ),
    },
    {
        "id": "fastapi_errors_1",
        "category": "backend",
        "text": (
            "FastAPI error handling best practice: raise HTTPException with appropriate status "
            "codes (400 for bad input, 401 for unauthorized, 404 for not found, 500 for server "
            "errors) instead of returning raw error strings. Always validate input with Pydantic "
            "schemas before processing."
        ),
    },
    {
        "id": "sql_security_1",
        "category": "database",
        "text": (
            "SQL security best practice: always use parameterized queries or an ORM like "
            "SQLAlchemy instead of string-concatenated SQL, to prevent SQL injection. Add "
            "indexes on columns that are frequently used in WHERE clauses or JOINs, such as "
            "foreign keys and columns used for filtering or sorting."
        ),
    },
    {
        "id": "sql_schema_1",
        "category": "database",
        "text": (
            "SQL schema design best practice: use UUID or SERIAL primary keys, add NOT NULL "
            "constraints on required fields, use foreign keys with appropriate ON DELETE "
            "behavior, and normalize tables to avoid data duplication. Add created_at and "
            "updated_at timestamp columns for auditing."
        ),
    },
    {
        "id": "react_structure_1",
        "category": "frontend",
        "text": (
            "React best practice: keep components small and focused on a single responsibility. "
            "Use functional components with hooks (useState, useEffect) instead of class "
            "components. Extract reusable logic into custom hooks. Keep API calls in separate "
            "files, not directly inside components."
        ),
    },
    {
        "id": "react_typescript_1",
        "category": "frontend",
        "text": (
            "React TypeScript best practice: define explicit interfaces for component props and "
            "API response shapes instead of using 'any'. Use optional chaining and default values "
            "to safely handle data that may not have loaded yet. Type event handlers explicitly, "
            "such as React.FormEvent for form submissions."
        ),
    },
    {
        "id": "react_styling_1",
        "category": "frontend",
        "text": (
            "React styling best practice with Tailwind CSS: use consistent spacing scale (4, 6, "
            "8 units), consistent color palette (e.g. indigo for primary actions, slate for "
            "neutral text), and ensure interactive elements like buttons have hover and disabled "
            "states for good user experience."
        ),
    },
]


def ingest():
    ids = [doc["id"] for doc in KNOWLEDGE_BASE]
    documents = [doc["text"] for doc in KNOWLEDGE_BASE]
    metadatas = [{"category": doc["category"]} for doc in KNOWLEDGE_BASE]

    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    print(f"Ingested {len(KNOWLEDGE_BASE)} knowledge base entries into ChromaDB.")


if __name__ == "__main__":
    ingest()
