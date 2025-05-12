WITH PlayerGoalStats AS (
  SELECT
    player_id,
    AVG(goals) AS avg_goals_per_game
  FROM Performance
  GROUP BY player_id
)
SELECT
  p.name,
  c.name AS club_name,
  pg.avg_goals_per_game
FROM PlayerGoalStats pg
JOIN Player p ON pg.player_id = p.player_id
JOIN Club c ON p.club_id = c.club_id
ORDER BY pg.avg_goals_per_game DESC;

