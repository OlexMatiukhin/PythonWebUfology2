ALTER TABLE users_custom
ADD COLUMN username VARCHAR(255),
ADD COLUMN email VARCHAR(255),
ADD COLUMN user_role VARCHAR(50),
ADD COLUMN birth_date DATE,
ADD COLUMN about_me TEXT,
ADD COLUMN is_blocked BOOLEAN,
ADD COLUMN user_password VARCHAR(255);


INSERT INTO users_custom (
    username,
    email,
    user_role,
    birth_date,
    about_me,
    is_blocked,
    user_password
) VALUES (
    'admin1',
    'admin@site.com',
    'admin',
    '1980-01-01',
    'Системний адміністратор від мами. Хто не вірить, в того сервер ляже, а хто вірить в того фаєрвол працюватиме проперлі.',
     FALSE,
    'admin'
);
select from  users_custom *;