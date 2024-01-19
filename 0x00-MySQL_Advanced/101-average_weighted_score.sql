-- task 13
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    ALTER TABLE users ADD total_weighted_score INT NOT NULL;
    ALTER TABLE users ADD total_weight INT NOT NULL;

    UPDATE users
    SET total_weighted_score = (
        SELECT SUM(corrections.score * projects.weight)
        FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = users.id
    );

    UPDATE users
    SET total_weight = (
        SELECT SUM(projects.weight)
        FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = users.id
    );

    UPDATE users
    SET average_score = IF(total_weight = 0, 0, total_weighted_score / total_weight);

    ALTER TABLE users
    DROP COLUMN total_weighted_score;
    ALTER TABLE users
    DROP COLUMN total_weight;
END $$
DELIMITER ;
