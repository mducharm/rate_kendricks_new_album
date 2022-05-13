CREATE TABLE "artists" (
	"id"	INTEGER,
	"name"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "albums" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"artist_id"	INTEGER NOT NULL,
	FOREIGN KEY("artist_id") REFERENCES "artists"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "songs" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"artist_id"	INTEGER NOT NULL,
	"album_id"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("album_id") REFERENCES "albums"("id"),
	FOREIGN KEY("artist_id") REFERENCES "artists"("id")
);