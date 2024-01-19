-- task 7
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    SELECT SUM(score) / COUNT(score) INTO @avgScore
    FROM corrections WHERE corrections.user_id=user_id;
    UPDATE users SET average_score=@avgScore WHERE id=user_id;
END;$$
