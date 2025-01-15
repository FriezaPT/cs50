SELECT m.title, r.rating FROM movies AS m JOIN ratings as r ON m.id = r.movie_id WHERE m.year = 2010 ORDER BY r.rating DESC, m.title ASC;
