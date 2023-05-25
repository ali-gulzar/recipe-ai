create table saved_recipes (
    user_id INTEGER NOT NULL REFERENCES users(id),
    recipe_id VARCHAR(255) NOT NULL,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)