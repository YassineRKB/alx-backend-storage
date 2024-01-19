-- task 12
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE total_weighted_score INT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
        INTO total_weighted_score, total_weight
        FROM corrections, projects
        WHERE corrections.project_id = projects.id
          AND corrections.user_id = user_id;

    UPDATE users
    SET average_score = IF(total_weight = 0, 0, total_weighted_score / total_weight)
    WHERE id = user_id;
END $$
DELIMITER ;
