create database project1;
use project1;

CREATE TABLE hall (
	hid INTEGER AUTO_INCREMENT PRIMARY KEY,
    h_name VARCHAR(10) NOT NULL UNIQUE,
    n_seats INTEGER DEFAULT 0
);

CREATE TABLE seat (
	type VARCHAR(10) PRIMARY KEY,
    price INTEGER NOT NULL
);

CREATE TABLE has_seats (
	hid INTEGER,
    sid INTEGER,
    type VARCHAR (10),
    FOREIGN KEY (hid) REFERENCES hall(hid) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (type) REFERENCES seat(type) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (hid, sid)
);

CREATE TABLE movie (
	mid INTEGER AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    rating VARCHAR(4) NOT NULL,
    descr VARCHAR(5000) NOT NULL,
    img VARCHAR(3000) NOT NULL,
    lang VARCHAR(15) NOT NULL,
    UNIQUE(title, lang)
);

CREATE TABLE movie_genre (
	mid INTEGER,
    genre VARCHAR(15),
    FOREIGN KEY (mid) REFERENCES movie(mid) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (mid, genre)
);

CREATE TABLE shows (
		hid INTEGER,
    mid INTEGER,
    time DATETIME NOT NULL,
    avail INTEGER DEFAULT 0,
    PRIMARY KEY (hid, mid, time),
    FOREIGN KEY (hid) REFERENCES hall(hid) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (mid) REFERENCES movie(mid) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE user (
	uid INTEGER AUTO_INCREMENT PRIMARY KEY,
	fname VARCHAR(20) NOT NULL,
	lname VARCHAR(20) NOT NULL,
	email VARCHAR(40) NOT NULL UNIQUE CHECK(email like "%@%.%"),
    phno VARCHAR(15),
    pass VARCHAR(20) NOT NULL CHECK(pass like "%______"),
    type VARCHAR(10) NOT NULL DEFAULT "normal"
);

CREATE TABLE booking (
    bid INTEGER AUTO_INCREMENT PRIMARY KEY,
	hid INTEGER NOT NULL,
    mid INTEGER NOT NULL,
    time DATETIME NOT NULL,
    uid INTEGER NOT NULL,
    n_seats INTEGER,
    FOREIGN KEY (hid, mid, time) REFERENCES shows(hid, mid, time) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE seats_booked (
	bid INTEGER,
    sid INTEGER,
    hid INTEGER,
    PRIMARY KEY (bid, sid, hid),
    FOREIGN KEY (bid) REFERENCES booking(bid) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (hid, sid) REFERENCES has_seats(hid, sid) ON DELETE CASCADE ON UPDATE CASCADE
);

DELIMITER //
CREATE TRIGGER h_seats AFTER INSERT ON has_seats
FOR EACH ROW
BEGIN
	UPDATE hall
		SET n_seats = n_seats+1
        WHERE hall.hid=NEW.hid;
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER new_show BEFORE INSERT ON shows
FOR EACH ROW
BEGIN
	DECLARE c INTEGER;
    SELECT COUNT(*) INTO c FROM has_seats WHERE has_seats.hid = NEW.hid;
	SET NEW.avail = c;
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER check_user AFTER INSERT ON user
FOR EACH ROW
BEGIN
	IF NEW.email NOT LIKE "%@%.%" THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Invalid email ID";
	ELSEIF NEW.pass NOT LIKE "______%" THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Invalid Password";
	END IF;
END; //
DELIMITER ;

INSERT INTO hall(h_name) VALUES("Audi 1");
INSERT INTO hall(h_name) VALUES("Audi 2");
INSERT INTO hall(h_name) VALUES("Audi 3");
INSERT INTO hall(h_name) VALUES("Audi 4");

INSERT INTO seat(type, price) VALUES ("Platinum", 250);
INSERT INTO seat(type, price) VALUES ("Gold", 200);
INSERT INTO seat(type, price) VALUES ("Silver", 150);

INSERT INTO has_seats(hid, sid, type) VALUES (1, 1, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (1, 2, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (1, 3, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (1, 4, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (1, 5, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (1, 6, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (1, 7, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (1, 8, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (1, 9, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (1, 10, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (1, 11, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (1, 12, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 1, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 2, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 3, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 4, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 5, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 6, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 7, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 8, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 9, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 10, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 11, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (2, 12, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 1, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 2, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 3, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 4, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 5, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 6, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 7, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 8, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 9, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 10, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 11, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (3, 12, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 1, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 2, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 3, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 4, "Platinum");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 5, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 6, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 7, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 8, "Gold");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 9, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 10, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 11, "Silver");
INSERT INTO has_seats(hid, sid, type) VALUES (4, 12, "Silver");

INSERT INTO movie(title, rating, lang,img) VALUES ("Colossal", "A", "English",'sda');
INSERT INTO movie(title, rating, lang,img) VALUES ("Ghost in the Shell", "A", "English",'asd');
INSERT INTO movie(title, rating, lang,img) VALUES ("The Boss Baby", "U/A", "English",'rgw');
INSERT INTO movie(title, rating, lang,img) VALUES ("Jolly LLB 2", "U/A", "Hindi",'sfgerg');
INSERT INTO movie(title, rating, lang,img) VALUES ("Dangal", "U/A", "Hindi",'asdfa');

INSERT INTO movie_genre(mid, genre) VALUES (5, "Biography");
INSERT INTO movie_genre(mid, genre) VALUES (5, "Sports");
INSERT INTO movie_genre(mid, genre) VALUES (5, "Drama");
INSERT INTO movie_genre(mid, genre) VALUES (4, "Comedy");
INSERT INTO movie_genre(mid, genre) VALUES (4, "Drama");
INSERT INTO movie_genre(mid, genre) VALUES (4, "Satire");
INSERT INTO movie_genre(mid, genre) VALUES (3, "Family");
INSERT INTO movie_genre(mid, genre) VALUES (3, "Comedy");
INSERT INTO movie_genre(mid, genre) VALUES (3, "Animation");
INSERT INTO movie_genre(mid, genre) VALUES (2, "Sci-Fi");
INSERT INTO movie_genre(mid, genre) VALUES (2, "Drama");
INSERT INTO movie_genre(mid, genre) VALUES (2, "Action");
INSERT INTO movie_genre(mid, genre) VALUES (1, "Thriller");
INSERT INTO movie_genre(mid, genre) VALUES (1, "Sci-Fi");
INSERT INTO movie_genre(mid, genre) VALUES (1, "Comedy");

INSERT INTO shows(hid, mid, time) VALUES (1, 1, "2017-04-12 19:30:00");
INSERT INTO shows(hid, mid, time) VALUES (2, 2, "2017-04-12 19:30:00");
INSERT INTO shows(hid, mid, time) VALUES (3, 3, "2017-04-12 19:30:00");
INSERT INTO shows(hid, mid, time) VALUES (4, 4, "2017-04-12 19:30:00");
INSERT INTO shows(hid, mid, time) VALUES (1, 4, "2017-04-12 22:00:00");
INSERT INTO shows(hid, mid, time) VALUES (2, 3, "2017-04-12 22:00:00");
INSERT INTO shows(hid, mid, time) VALUES (3, 3, "2017-04-12 22:00:00");
INSERT INTO shows(hid, mid, time) VALUES (4, 4, "2017-04-12 22:00:00");
INSERT INTO shows(hid, mid, time) VALUES (1, 5, "2017-04-12 17:00:00");
INSERT INTO shows(hid, mid, time) VALUES (2, 3, "2017-04-12 17:00:00");

INSERT INTO user(fname, lname, email, pass, phno, type) VALUES ("Naman", "Maheshwari", "naman1901@gmail.com", "password", "9716555025", "Admin");
INSERT INTO user(fname, lname, email, pass, phno, type) VALUES ("Mohit", "Sharma", "iammohitsharma@gmail.com", "password", "9958832882", "Admin");
INSERT INTO user(fname, lname, email, pass, phno, type) VALUES ("Jeevesh", "Narang", "narang.jeevesh@gmail.com", "password", "9654832882", "Admin");
INSERT INTO user(fname, lname, email, pass, phno, type) VALUES ("Kunal", "Kardam", "kunal.kardam@gmail.com", "password", "9678923455", "User");

UPDATE movie SET descr = "After losing her job and boyfriend in New York City, Gloria (Anne Hathaway) moves back to her hometown in upstate New York only to discover how strangely connected she is to an enormous giant monster attacking Seoul, South Korea." where mid = 1;
UPDATE movie SET descr = "Ghost in the Shell is a 2017 American science fiction action film directed by Rupert Sanders and written by Jamie Moss, William Wheeler and Ehren Kruger, based on the Japanese manga of the same name by Masamune Shirow. The film stars Scarlett Johansson, Takeshi Kitano, Michael Pitt, Pilou Asbæk, Chin Han and Juliette Binoche. Set in the near future where the line between humans and robots is becoming blurred, the plot follows a woman who has her brain placed in a cyborg body to become the perfect soldier and who yearns to learn of her past." where mid = 2;
UPDATE movie SET descr = "The Boss Baby is a 2017 American computer-animated comedy film, loosely based on the 2010 picture book of the same name written and illustrated by Marla Frazee. Produced by DreamWorks Animation, the film is directed by Tom McGrath and written by Michael McCullers. It stars the voices of Alec Baldwin, Miles Christopher Bakshi, Steve Buscemi, Jimmy Kimmel, Lisa Kudrow and Tobey Maguire. The plot follows a baby who is a secret agent in the secret war between babies and puppies." where mid = 3;
UPDATE movie SET descr = "The State vs Jolly LL.B 2, known also as Jolly LL.B 2, is a 2017 Indian black comedy film, written and directed by Subhash Kapoor. A sequel to the 2013 film Jolly LLB, and the second installment of Jolly LLB (film series). The film stars Akshay Kumar, Huma Qureshi, Saurabh Shukla and Annu Kapoor in lead roles. A courtroom drama which satirizes the notion of the Indian legal system, the story follows Jagdishwar Mishra (Akshay Kumar), a lawyer who fights a case against the ruthless and powerful lawyer Pramod Mathur (Annu Kapoor)." where mid = 4;
UPDATE movie SET descr = "Dangal (English: Wrestling competition) is a 2016 Indian Hindi-language biographical sports drama film directed by Nitesh Tiwari. It stars Aamir Khan as Mahavir Singh Phogat, who taught wrestling to his daughters Geeta Phogat and Babita Kumari. The former is India's first female wrestler to win at the 2010 Commonwealth Games, where she won the gold medal (55 kg). Her sister Babita Kumari won the silver (51 kg)." where mid = 5;
