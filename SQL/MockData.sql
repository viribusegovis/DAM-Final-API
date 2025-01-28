USE [db-dam-final]
-- Inserir utilizadores de teste
INSERT INTO users (email, password, name, created_at, last_login, is_active) VALUES
('joao@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY', 'João Silva', GETDATE(), GETDATE(), 1),
('maria@email.com', '$2b$12$9kLqoEbzPgq5RxMGZJxQ2eKzJ3QZ1jD5tN8oL2pY', 'Maria Santos', GETDATE(), GETDATE(), 1),
('antonio@email.com', '$2b$12$4mN2p8qKxLwQ9RzHjPkL5eXzJ1tN8oL2pYz6TtxM', 'António Ferreira', GETDATE(), GETDATE(), 1);

-- Inserir categorias
INSERT INTO categories (name, description, image_url) VALUES
('Pratos Principais', 'Refeições completas e substanciais', 'pratos_principais.jpg'),
('Sobremesas', 'Doces e sobremesas tradicionais', 'sobremesas.jpg'),
('Sopas', 'Sopas e caldos tradicionais', 'sopas.jpg'),
('Entradas', 'Aperitivos e petiscos', 'entradas.jpg'),
('Vegetariano', 'Pratos sem carne ou peixe', 'vegetariano.jpg');

-- Inserir receitas
INSERT INTO recipes (title, description, preparation_time, servings, difficulty, image_url, author_id, category_id, created_at) VALUES
('Bacalhau à Brás', 'Prato tradicional português com bacalhau desfiado', 45, 4, 'MEDIO', 'bacalhau_bras.jpg', 1, 1, GETDATE()),
('Pastéis de Nata', 'Sobremesa típica portuguesa', 60, 12, 'DIFICIL', 'pasteis_nata.jpg', 2, 2, GETDATE()),
('Caldo Verde', 'Sopa tradicional portuguesa', 30, 6, 'FACIL', 'caldo_verde.jpg', 1, 3, GETDATE()),
('Arroz de Legumes', 'Prato vegetariano saudável', 35, 4, 'FACIL', 'arroz_legumes.jpg', 3, 5, GETDATE());

-- Inserir relações receita-categoria
INSERT INTO recipe_categories (recipe_id, category_id) VALUES
(1, 1), -- Bacalhau: Pratos Principais
(2, 2), -- Pastéis: Sobremesas
(3, 3), -- Caldo Verde: Sopas
(3, 1), -- Caldo Verde: Pratos Principais
(4, 5), -- Arroz: Vegetariano
(4, 1); -- Arroz: Pratos Principais

-- Inserir ingredientes
INSERT INTO ingredients (name) VALUES
('Bacalhau'),
('Batata Palha'),
('Ovos'),
('Azeite'),
('Couve Galega'),
('Massa Folhada'),
('Leite'),
('Canela'),
('Arroz'),
('Cenoura');

-- Inserir ingredientes das receitas
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit) VALUES
(1, 1, 400, 'gramas'),
(1, 2, 200, 'gramas'),
(1, 3, 6, 'unidades'),
(2, 3, 4, 'unidades'),
(2, 6, 500, 'gramas'),
(3, 4, 50, 'ml'),
(3, 5, 200, 'gramas'),
(4, 9, 300, 'gramas'),
(4, 10, 150, 'gramas');

-- Inserir instruções
INSERT INTO instructions (recipe_id, step_number, instruction_text) VALUES
(1, 1, 'Desfie o bacalhau em lascas pequenas'),
(1, 2, 'Misture os ovos batidos com o bacalhau'),
(1, 3, 'Adicione a batata palha e envolva bem'),
(2, 1, 'Prepare a massa folhada'),
(2, 2, 'Faça o creme de pastel de nata'),
(2, 3, 'Leve ao forno a 250°C'),
(3, 1, 'Coza as batatas'),
(3, 2, 'Corte a couve em juliana fina'),
(3, 3, 'Adicione um fio de azeite no final'),
(4, 1, 'Coza o arroz em água temperada'),
(4, 2, 'Salteie os legumes cortados'),
(4, 3, 'Misture os legumes com o arroz');
