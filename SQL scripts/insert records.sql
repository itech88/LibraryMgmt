use library;

INSERT INTO Books (title, author, publish_date, available) VALUES ('book', 'author', NULL, TRUE);
INSERT INTO Books (title, author, publish_date, available) VALUES ('Lord of the Rings', 'JRR Tolkien', NULL, TRUE);
INSERT INTO Books (title, author, publish_date, available) VALUES ('The Hobbit', 'JRR Tolkien', NULL, TRUE);
INSERT INTO Books (title, author, publish_date, available) VALUES ('Tom Sawyer', 'Mark Twain', NULL, TRUE);
INSERT INTO Books (title, author, publish_date, available) VALUES ('Huckleberry Finn', 'Mark Twain', NULL, TRUE);



-- Step 1: Add 'copies' column
ALTER TABLE Books
ADD copies INT NOT NULL DEFAULT 0;

-- Step 2: Add 'checked_out' column
ALTER TABLE Books
ADD checked_out INT NOT NULL DEFAULT 0;

-- Step 3: Drop 'available' column if it exists
ALTER TABLE Books
DROP COLUMN IF EXISTS available;

-- Step 4: Add 'available' column as a virtual column
ALTER TABLE Books
ADD available BOOLEAN AS (copies > checked_out) VIRTUAL;

-- Step 5: Add 'is_checked_out' column as a virtual column
ALTER TABLE Books
ADD is_checked_out BOOLEAN AS (checked_out > 0) VIRTUAL;
