-- Keep a log of any SQL queries you execute as you solve the mystery.
-- First one is to understand the table organization
.schema

-- Get the crime scene report for that time and place
SELECT * FROM crime_scene_reports WHERE year = 2023 AND month = 7 AND day = 28 AND street LIKE "Humphrey%";

-- After getting the information, i now know that three witnesses were present and their transcripts mention the bakery and that it occured at 10.15am. There is also information that in that day, in the afternoon, someone littered with no witnesses.
-- Now i'll go check the interviews
SELECT * FROM interviews WHERE year = 2023 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";

-- +-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
-- | id  |  name   | year | month | day |                                                                                                                                                     transcript                                                                                                                                                      |
-- +-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
-- | 161 | Ruth    | 2023 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
-- | 162 | Eugene  | 2023 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
-- | 163 | Raymond | 2023 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
-- +-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

-- The results show some important information: The thief got on a car that was parked around the time of the theft,
-- The thief was recognized by Eugene,
-- the thief was on an ATM on Leggett Street that day earlier and made a call to someone for less than a minute.
-- In that call he/she said to the other person to buy the ticket

-- I'll start by trying to get the licence plate of the car
SELECT * FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour < 11;

-- From this query we get that the car that exited closer to the robbery had the plate 5P2BI95 and entered the parking lot at 9.15. Seems important but a dead end.
-- Now i'll check the ATM on Leggett Street for that day.
SELECT * FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location LIKE "Leggett%";

-- +-----+----------------+------+-------+-----+----------------+------------------+--------+
-- | id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
-- +-----+----------------+------+-------+-----+----------------+------------------+--------+
-- | 246 | 28500762       | 2023 | 7     | 28  | Leggett Street | withdraw         | 48     |
-- | 264 | 28296815       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
-- | 266 | 76054385       | 2023 | 7     | 28  | Leggett Street | withdraw         | 60     |
-- | 267 | 49610011       | 2023 | 7     | 28  | Leggett Street | withdraw         | 50     |
-- | 269 | 16153065       | 2023 | 7     | 28  | Leggett Street | withdraw         | 80     |
-- | 275 | 86363979       | 2023 | 7     | 28  | Leggett Street | deposit          | 10     |
-- | 288 | 25506511       | 2023 | 7     | 28  | Leggett Street | withdraw         | 20     |
-- | 313 | 81061156       | 2023 | 7     | 28  | Leggett Street | withdraw         | 30     |
-- | 336 | 26013199       | 2023 | 7     | 28  | Leggett Street | withdraw         | 35     |
-- +-----+----------------+------+-------+-----+----------------+------------------+--------+

-- It doesn't yeald much information as there are no hours, but the account number may be helpfull for later.
-- Now i'll check phone calls that day, to see if i can gather information there.
SELECT * FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2023 AND duration < 60;

-- That query yelded:
-- +-----+----------------+----------------+------+-------+-----+----------+
-- | id  |     caller     |    receiver    | year | month | day | duration |
-- +-----+----------------+----------------+------+-------+-----+----------+
-- | 221 | (130) 555-0289 | (996) 555-8899 | 2023 | 7     | 28  | 51       |
-- | 224 | (499) 555-9472 | (892) 555-8872 | 2023 | 7     | 28  | 36       |
-- | 233 | (367) 555-5533 | (375) 555-8161 | 2023 | 7     | 28  | 45       |
-- | 251 | (499) 555-9472 | (717) 555-1342 | 2023 | 7     | 28  | 50       |
-- | 254 | (286) 555-6063 | (676) 555-6554 | 2023 | 7     | 28  | 43       |
-- | 255 | (770) 555-1861 | (725) 555-3243 | 2023 | 7     | 28  | 49       |
-- | 261 | (031) 555-6622 | (910) 555-3251 | 2023 | 7     | 28  | 38       |
-- | 279 | (826) 555-1652 | (066) 555-9701 | 2023 | 7     | 28  | 55       |
-- | 281 | (338) 555-6650 | (704) 555-2131 | 2023 | 7     | 28  | 54       |
-- +-----+----------------+----------------+------+-------+-----+----------+

-- At this point, i just realised that i can search a person by it's licence plate and will try to do that with the what we got on the other query
SELECT * FROM people WHERE license_plate = '5P2BI95';

-- +--------+---------+----------------+-----------------+---------------+
-- |   id   |  name   |  phone_number  | passport_number | license_plate |
-- +--------+---------+----------------+-----------------+---------------+
-- | 221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95       |
-- +--------+---------+----------------+-----------------+---------------+

-- Now i can improve the query for phone records to check if any phone call was made that day

SELECT * FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2023 AND duration < 60 AND (caller = '(725) 555-4692' OR receiver = '(725) 555-4692');

-- My assumption of the licence_plate probably was missguided as there is no call record with that person's number. I'll do a nested query to check if there is someone that matches the criteria
-- Car leaving after the theft, phone call less than one minute in that day.

SELECT * FROM phone_calls
WHERE day = 28
AND month = 7
AND year = 2023
AND duration < 60
AND caller IN (SELECT phone_number FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10));

-- +-----+----------------+----------------+------+-------+-----+----------+
-- | id  |     caller     |    receiver    | year | month | day | duration |
-- +-----+----------------+----------------+------+-------+-----+----------+
-- | 221 | (130) 555-0289 | (996) 555-8899 | 2023 | 7     | 28  | 51       |
-- | 224 | (499) 555-9472 | (892) 555-8872 | 2023 | 7     | 28  | 36       |
-- | 233 | (367) 555-5533 | (375) 555-8161 | 2023 | 7     | 28  | 45       |
-- | 251 | (499) 555-9472 | (717) 555-1342 | 2023 | 7     | 28  | 50       |
-- | 254 | (286) 555-6063 | (676) 555-6554 | 2023 | 7     | 28  | 43       |
-- | 255 | (770) 555-1861 | (725) 555-3243 | 2023 | 7     | 28  | 49       |
-- +-----+----------------+----------------+------+-------+-----+----------+


-- Now i should go back, and check if any of the people with these number and phone numbers were at the ATM in that street in that day.

SELECT * FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location LIKE "Leggett%" AND account_number IN(
    SELECT account_number FROM bank_accounts WHERE person_id IN (
        SELECT id FROM people WHERE phone_number IN(
            SELECT caller FROM phone_calls
            WHERE day = 28
            AND month = 7
            AND year = 2023
            AND duration < 60
            AND caller IN (SELECT phone_number FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10))
            )
        )
);

-- +-----+----------------+------+-------+-----+----------------+------------------+--------+
-- | id  | account_number | year | month | day |  atm_location  | transaction_type | amount |
-- +-----+----------------+------+-------+-----+----------------+------------------+--------+
-- | 266 | 76054385       | 2023 | 7     | 28  | Leggett Street | withdraw         | 60     |
-- | 267 | 49610011       | 2023 | 7     | 28  | Leggett Street | withdraw         | 50     |
-- | 336 | 26013199       | 2023 | 7     | 28  | Leggett Street | withdraw         | 35     |
-- +-----+----------------+------+-------+-----+----------------+------------------+--------+


-- Now we're left with three possible people that meet all the criteria.
-- We can check the flights from fiftyville from that date on and try to match one of the suspects
-- I will start by querying simply to get the id of the airport of fiftyville, to limit the size of subsequent queries, since it's a static value
SELECT * from airports WHERE city = 'Fiftyville';

-- +----+--------------+-----------------------------+------------+
-- | id | abbreviation |          full_name          |    city    |
-- +----+--------------+-----------------------------+------------+
-- | 8  | CSF          | Fiftyville Regional Airport | Fiftyville |
-- +----+--------------+-----------------------------+------------+

-- Now with that information i can check the eariler flight to depart from there the next day
SELECT * FROM flights WHERE origin_airport_id = 8 AND year = 2023 AND month = 7 AND day = 29 ORDER BY hour ASC;


-- +----+-------------------+------------------------+------+-------+-----+------+--------+
-- | id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
-- +----+-------------------+------------------------+------+-------+-----+------+--------+
-- | 36 | 8                 | 4                      | 2023 | 7     | 29  | 8    | 20     |
-- | 43 | 8                 | 1                      | 2023 | 7     | 29  | 9    | 30     |
-- | 23 | 8                 | 11                     | 2023 | 7     | 29  | 12   | 15     |
-- | 53 | 8                 | 9                      | 2023 | 7     | 29  | 15   | 20     |
-- | 18 | 8                 | 6                      | 2023 | 7     | 29  | 16   | 0      |
-- +----+-------------------+------------------------+------+-------+-----+------+--------+

-- Now we know the flight id and can check if any of those people are on the passenger list for that flight
SELECT * FROM passengers WHERE flight_id = 36 AND passport_number IN(
    SELECT passport_number FROM people WHERE id IN(
        SELECT person_id FROM bank_accounts WHERE account_number IN (
            SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location LIKE "Leggett%" AND account_number IN(
                SELECT account_number FROM bank_accounts WHERE person_id IN (
                    SELECT id FROM people WHERE phone_number IN(
                        SELECT caller FROM phone_calls
                        WHERE day = 28
                        AND month = 7
                        AND year = 2023
                        AND duration < 60
                        AND caller IN (SELECT phone_number FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10))
                        )
                    )
            )
        )
    )
);

-- +-----------+-----------------+------+
-- | flight_id | passport_number | seat |
-- +-----------+-----------------+------+
-- | 36        | 5773159633      | 4A   |
-- | 36        | 1988161715      | 6D   |
-- +-----------+-----------------+------+


-- We are left with two people. Going back i think i need to redo the query to account for the 10m interval for the car to leave the parking lot.
SELECT * FROM passengers WHERE flight_id = 36 AND passport_number IN(
    SELECT passport_number FROM people WHERE id IN(
        SELECT person_id FROM bank_accounts WHERE account_number IN (
            SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location LIKE "Leggett%" AND account_number IN(
                SELECT account_number FROM bank_accounts WHERE person_id IN (
                    SELECT id FROM people WHERE phone_number IN(
                        SELECT caller FROM phone_calls
                        WHERE day = 28
                        AND month = 7
                        AND year = 2023
                        AND duration < 60
                        AND caller IN (SELECT phone_number FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND (minute < 25 AND minute > 15)))
                        )
                    )
            )
        )
    )
);


-- +-----------+-----------------+------+
-- | flight_id | passport_number | seat |
-- +-----------+-----------------+------+
-- | 36        | 5773159633      | 4A   |
-- +-----------+-----------------+------+

-- We are now left with the passport number of the thief. Now it's just a matter to query the people table to get his/her name.
SELECT * FROM people WHERE passport_number = 5773159633;

-- +--------+-------+----------------+-----------------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate |
-- +--------+-------+----------------+-----------------+---------------+
-- | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
-- +--------+-------+----------------+-----------------+---------------+

-- To answer the next question of the city he escaped to, we just need to check the destination airport of the flight
SELECT * FROM airports WHERE id = 4;

-- +----+--------------+-------------------+---------------+
-- | id | abbreviation |     full_name     |     city      |
-- +----+--------------+-------------------+---------------+
-- | 4  | LGA          | LaGuardia Airport | New York City |
-- +----+--------------+-------------------+---------------+

-- Now for the answer of the accomplice, we need to check the receiver of his call at the time of the robbery. I will use the information gathered above to make the query simpler.
SELECT * FROM people WHERE phone_number = '(375) 555-8161';

-- +--------+-------+----------------+-----------------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate |
-- +--------+-------+----------------+-----------------+---------------+
-- | 864400 | Robin | (375) 555-8161 | NULL            | 4V16VO0       |
-- +--------+-------+----------------+-----------------+---------------+
