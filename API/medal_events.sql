USE olympics;

CREATE TABLE medal_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_date DATE,
    discipline_name VARCHAR(255),
    medal VARCHAR(50)
);

SELECT * FROM medal_events;




