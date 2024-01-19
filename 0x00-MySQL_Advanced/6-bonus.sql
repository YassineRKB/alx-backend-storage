-- task 6
DELIMITER $$

CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
    INSERT INTO projects (name) SELECT project_name AS name FROM (SELECT project_name) AS temp
    WHERE NOT EXISTS (SELECT name FROM projects WHERE name=project_name);

    SELECT id INTO @project_id FROM projects WHERE name=project_name;
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, @project_id, score);
END;$$
