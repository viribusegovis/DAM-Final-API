CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(255) NOT NULL UNIQUE,
    password NVARCHAR(255) NOT NULL,
    name NVARCHAR(255) NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    last_login DATETIME2,
    is_active BIT DEFAULT 1
);

CREATE TABLE recipes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    preparation_time INT NOT NULL,
    servings INT NOT NULL,
    difficulty NVARCHAR(10) CHECK (difficulty IN ('FACIL', 'MEDIO', 'DIFICIL')),
    image_url NVARCHAR(MAX),
    author_id INT NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    category NVARCHAR(100) NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE instructions (
    instruction_id INT IDENTITY(1,1) PRIMARY KEY,
    recipe_id INT NOT NULL,
    step_number INT NOT NULL,
    instruction_text NVARCHAR(MAX) NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

CREATE TABLE ingredients (
    ingredient_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE recipe_ingredients (
    recipe_id INT NOT NULL,
    ingredient_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    unit NVARCHAR(50) NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON DELETE CASCADE,
    PRIMARY KEY (recipe_id, ingredient_id)
);

