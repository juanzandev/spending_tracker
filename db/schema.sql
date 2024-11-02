CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    spending_score DECIMAL(3,1) DEFAULT 5,
);

CREATE TABLE Transactions (
    user_id INT REFERENCES Users(user_id),
    transaction_id SERIAL,
    date DATE NOT NULL,
    description VARCHAR(255),
    transaction_type VARCHAR(50),
    amount DECIMAL(10, 2),
    category VARCHAR(50),
    payment_method VARCHAR(50),
    merchant VARCHAR(100),
    balance DECIMAL(10, 2),
    PRIMARY KEY (user_id, transaction_id)
);

CREATE TABLE IF NOT EXISTS Budgets (
    budget_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    category VARCHAR(50),
    monthly_limit DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS Rewards (
    reward_id SERIAL PRIMARY KEY,
    score_range VARCHAR(20),
    reward_description TEXT
);

CREATE TABLE IF NOT EXISTS SpendingPatterns (
    pattern_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    month DATE NOT NULL,
    total_spent DECIMAL(10,2) NOT NULL,
    total_income DECIMAL(10, 2) NOT NULL
);