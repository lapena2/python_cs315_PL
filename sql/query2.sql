SELECT name
FROM Player
WHERE player_id IN (
  SELECT player_id
  FROM Performance
  WHERE game_id = 1 AND goals > 0
);

