-- Insert test users
INSERT INTO users (email, password, name, created_at, last_login, is_active) VALUES
('joao@email.com', 'hashed_password_123', 'João Silva', GETDATE(), GETDATE(), 1),
('maria@email.com', 'hashed_password_456', 'Maria Santos', GETDATE(), GETDATE(), 1),
('antonio@email.com', 'hashed_password_789', 'António Ferreira', GETDATE(), GETDATE(), 1);

-- Insert test recipes
INSERT INTO recipes (title, description, preparation_time, servings, difficulty, image_url, author_id, category) VALUES
('Bacalhau à Brás', 'Prato tradicional português com bacalhau desfiado', 45, 4, 'MEDIO', 'bacalhau_bras.jpg', 1, 'Pratos Principais'),
('Pastéis de Nata', 'Sobremesa típica portuguesa', 60, 12, 'DIFICIL', 'pasteis_nata.jpg', 2, 'Sobremesas'),
('Caldo Verde', 'Sopa tradicional portuguesa', 30, 6, 'FACIL', 'caldo_verde.jpg', 1, 'Sopas');

-- Insert test ingredients
INSERT INTO ingredients (name) VALUES
('Bacalhau'),
('Batata palha'),
('Ovos'),
('Azeite'),
('Couve'),
('Massa folhada'),
('Leite'),
('Canela');

-- Insert test recipe_ingredients
INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit) VALUES
(1, 1, 400, 'gramas'),
(1, 2, 200, 'gramas'),
(1, 3, 6, 'unidades'),
(2, 3, 4, 'unidades'),
(2, 6, 500, 'gramas'),
(3, 4, 50, 'ml'),
(3, 5, 200, 'gramas');

-- Insert test instructions
INSERT INTO instructions (recipe_id, step_number, instruction_text) VALUES
(1, 1, 'Desfie o bacalhau em lascas pequenas'),
(1, 2, 'Misture os ovos batidos com o bacalhau'),
(1, 3, 'Adicione a batata palha e envolva bem'),
(2, 1, 'Prepare a massa folhada'),
(2, 2, 'Faça o creme de pastel de nata'),
(2, 3, 'Leve ao forno a 250ºC'),
(3, 1, 'Coza as batatas'),
(3, 2, 'Corte a couve em juliana fina'),
(3, 3, 'Adicione um fio de azeite no final');
