
Use comp267;

SELECT * FROM department;

SELECT * FROM topic;

SELECT * FROM gov_website;


-- INSERT TEST RECORDS

-- Insert a new department
INSERT INTO department (name, description)
VALUES ('Test Department', 'This is a test department.');

-- Insert a new topic
INSERT INTO topic (name, description)
VALUES ('Test Topic', 'This is a test topic.');

-- Insert a new website linked to the test department and topic
INSERT INTO gov_website (name, url, department_id, topic_id)
VALUES ('Test Website', 'https://example.com/test', 
        (SELECT department_id FROM department WHERE name='Test Department'),
        (SELECT topic_id FROM topic WHERE name='Test Topic'));

-- Verify insertion
SELECT * FROM gov_website WHERE name='Test Website';


-- UPDATING


-- Update the website URL
UPDATE gov_website
SET url='https://example.com/test-updated'
WHERE name='Test Website';

-- Update the topic name
UPDATE topic
SET name='Test Topic Updated'
WHERE name='Test Topic';

-- Verify updates
SELECT g.name, g.url, d.name AS department_name, t.name AS topic_name
FROM gov_website g
JOIN department d ON g.department_id=d.department_id
JOIN topic t ON g.topic_id=t.topic_id
WHERE g.name='Test Website';


-- DELETE


-- Delete the test website
DELETE FROM gov_website
WHERE name='Test Website';

-- Delete the test topic
DELETE FROM topic
WHERE name='Test Topic Updated';

-- Delete the test department
DELETE FROM department
WHERE name='Test Department';

-- Verify deletion
SELECT * FROM department WHERE name='Test Department';
SELECT * FROM topic WHERE name='Test Topic Updated';
SELECT * FROM gov_website WHERE name='Test Website';


-- QUERY TESTS FOR EXISTING DATA


-- List all websites with department and topic names
SELECT g.name AS website_name, g.url, d.name AS department_name, t.name AS topic_name
FROM gov_website g
JOIN department d ON g.department_id = d.department_id
JOIN topic t ON g.topic_id = t.topic_id
ORDER BY g.website_id;

-- Count websites per department
SELECT d.name AS department_name, COUNT(*) AS num_websites
FROM gov_website g
JOIN department d ON g.department_id = d.department_id
GROUP BY d.name
ORDER BY num_websites DESC;

-- Search for websites containing 'Parks'
SELECT * FROM gov_website
WHERE name LIKE '%Parks%';

-- Check topic assignments for 'NCDMV Driver License / ID Renewal Online'
SELECT g.name AS website_name, t.name AS topic_name
FROM gov_website g
JOIN topic t ON g.topic_id = t.topic_id
WHERE g.name='NCDMV Driver License / ID Renewal Online';

