SELECT
  p.name AS player_name,
  c.name AS club_name,
  SUM(perf.goals) AS total_goals
FROM Performance perf
JOIN Player p ON perf.player_id = p.player_id
JOIN Club c ON p.club_id = c.club_id
GROUP BY p.name, c.name
ORDER BY total_goals DESC;


