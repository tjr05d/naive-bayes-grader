--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.4
-- Dumped by pg_dump version 9.5.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: whoisjose04
--

CREATE TABLE categories (
    id integer NOT NULL,
    title character varying,
    feedback text,
    question_id integer
);


ALTER TABLE categories OWNER TO whoisjose04;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: whoisjose04
--

CREATE SEQUENCE categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE categories_id_seq OWNER TO whoisjose04;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: whoisjose04
--

ALTER SEQUENCE categories_id_seq OWNED BY categories.id;


--
-- Name: questions; Type: TABLE; Schema: public; Owner: whoisjose04
--

CREATE TABLE questions (
    id integer NOT NULL,
    title character varying,
    prompt text,
    unit_id integer
);


ALTER TABLE questions OWNER TO whoisjose04;

--
-- Name: questions_id_seq; Type: SEQUENCE; Schema: public; Owner: whoisjose04
--

CREATE SEQUENCE questions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE questions_id_seq OWNER TO whoisjose04;

--
-- Name: questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: whoisjose04
--

ALTER SEQUENCE questions_id_seq OWNED BY questions.id;


--
-- Name: responses; Type: TABLE; Schema: public; Owner: whoisjose04
--

CREATE TABLE responses (
    id integer NOT NULL,
    answer text,
    role character varying,
    categories_id integer,
    questions_id integer
);


ALTER TABLE responses OWNER TO whoisjose04;

--
-- Name: responses_id_seq; Type: SEQUENCE; Schema: public; Owner: whoisjose04
--

CREATE SEQUENCE responses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE responses_id_seq OWNER TO whoisjose04;

--
-- Name: responses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: whoisjose04
--

ALTER SEQUENCE responses_id_seq OWNED BY responses.id;


--
-- Name: units; Type: TABLE; Schema: public; Owner: whoisjose04
--

CREATE TABLE units (
    id integer NOT NULL,
    title character varying,
    description text
);


ALTER TABLE units OWNER TO whoisjose04;

--
-- Name: units_id_seq; Type: SEQUENCE; Schema: public; Owner: whoisjose04
--

CREATE SEQUENCE units_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE units_id_seq OWNER TO whoisjose04;

--
-- Name: units_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: whoisjose04
--

ALTER SEQUENCE units_id_seq OWNED BY units.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY categories ALTER COLUMN id SET DEFAULT nextval('categories_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY questions ALTER COLUMN id SET DEFAULT nextval('questions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY responses ALTER COLUMN id SET DEFAULT nextval('responses_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY units ALTER COLUMN id SET DEFAULT nextval('units_id_seq'::regclass);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: whoisjose04
--

COPY categories (id, title, feedback, question_id) FROM stdin;
11	Correct 	blah blah blah 	9
12	Incorrect	Not right	9
13	No markdown 	Please use markdown	9
14	Correct	Nice Work! You're starting to get the hang of this JavaScript stuff :) 	14
15	Correct, but used `hasOwnProperty`	Nice, this works. However the `hasOwnProperty` line seems a unnecessary as the for loop should only iterate over items that are included in the array. 	14
16	Correct, uses forEach and function	Great this is an interesting way to accomplish the task. another way that would have worked is ```js var a = { one: 1, two: 2, three: 3, four: 4, five: 5 }; for (var i in a){   console.log(i, ':', a[i]) }```	14
17	Missing Array	currently a is undefined, please define that array before using it in a loop. 	14
18	Incorrect,  undefined variable	It looks like you have an undefined variable	14
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: whoisjose04
--

SELECT pg_catalog.setval('categories_id_seq', 18, true);


--
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: whoisjose04
--

COPY questions (id, title, prompt, unit_id) FROM stdin;
1	Sam I am	\N	\N
2	Array Of Light Part 2	For these three questions, you'll be using the code below to work some magic on Arrays!\n\n```ruby\n[[1,2,3],[4,5,6]]\n```\n\nReturn the largest number from the array.	\N
9	Distributive Properties	\nDistribute the value outside the parentheses to simplify the statement.\n\nFor instance: `-(10 + 20)` == `-10 - 20`\n\n```ruby\n-(1 - 1)\nnot(true or false)\n-(-1+1)\nnot(!true and false)\n```	\N
14	For JavaScript's Sake	Fix this loop so that it enumerates all of the key/value pairs.\n\n```js\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\nfor (var i = 0, len = a.length; i < len; i++ ){\n  console.log(i, a[i]);\n}\n```\n\nJSON objects have no length, so `a.length` is undefined and the loop doesn’t execute. There's another type of `for` loop that helps us easily loop over all of the objects in a collection. 	\N
15	Converting Data Types And Concatenating	Let's do a couple more things we take for granted in Ruby: convert something to another data type and concatenate strings!\n\nImplement this in javascript:\n\n```ruby\nnumber_of_hoverboards = "1"\nputs "There are at least #{number_of_hoverboards}  hoverboard(s) in 2015."\nnumber_of_hoverboards = number_of_hoverboards.to_i\nnumber_of_hoverboards -= 1\n\nputs "There are at least #{number_of_hoverboards}  hoverboard(s) in 2015."\n```\nImportant to note: Make sure to use JavaScript naming best practices, instead of Ruby best practices.	\N
\.


--
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: whoisjose04
--

SELECT pg_catalog.setval('questions_id_seq', 15, true);


--
-- Data for Name: responses; Type: TABLE DATA; Schema: public; Owner: whoisjose04
--

COPY responses (id, answer, role, categories_id, questions_id) FROM stdin;
77	```javascript\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\nfor (var key in a) { \r\nconsole.log(key + ' : ' + a[key]);\r\n}\r\n```	\N	\N	14
84	```javascript\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\nfor (var i in a) {\n  console.log(i + ": " + a[i]);\n}\n```	\N	\N	14
86	```js\r\n\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\n\r\nfor (i in a) {\r\n  console.log(i+ ":" + " "+a[i]);\r\n}\r\n\r\n\r\n```	\N	\N	14
87	```js\r\n\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\n  for (i in a) {\r\n  console.log(i, a[i]);\r\n}\r\n\r\n\r\n```	\N	\N	14
89	```javascript\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\n\r\nfor (var prop in a){\r\n   console.log(prop + " = " + obj[prop]);\r\n}\r\n```	\N	\N	14
90	```javascript\r\nvar a = { one: 1,\r\n          two: 2,\r\n          three: 3,\r\n          four: 4,\r\n          five: 5\r\n        };\r\n\r\nfor (var key in a) {\r\n  console.log("key:" + key + "," + " value:" + a[key]);\r\n}\r\n```	\N	\N	14
91	```javascript\r\nfor (key in a) {\r\n  console.log(key + ": " + a[key]);\r\n}\r\n```	\N	\N	14
92	```javascript\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\nfor (var i in a){\n  console.log(i, a[i]);\n}\n```	\N	\N	14
93	```javascript\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\nfor (var i in a){\n   console.log(i, a[i]);\n}\n```	\N	\N	14
108	```javascript\nvar numberOfHoverboards = "1";\nconsole.log("There are at least " + numberOfHoverboards +   " hoverboard(s) in 2015.");\n\nvar numberOfHoverboards = parseInt(numberOfHoverboards);\nvar numberOfHoverboards = numberOfHoverboards - 1;\n\nconsole.log("There are at least " + numberOfHoverboards +   " hoverboard(s) in 2015.");\n```\n\n=> There are at least 1 hoverboard(s) in 2015.\n=> There are at least 0 hoverboard(s) in 2015.	\N	\N	15
109	```javascript\r\nnumberOfHoverboards = "1";\r\nconsole.log("There are at least " + numberOfHoverboards + " hoverboard(s) in 2015.";\r\nnumberOfHoverboards -= 1;\r\nconsole.log("There are at least " + numberOfHoverboard + " hoverboard(s) in 2015.");	\N	\N	15
110	```javascript\r\n\r\n var numberOfHoverboards = "1" ;\r\nconsole.log ("There are at least " + numberOfHoverboards + " hoverboard(s) in 2015.");\r\n numberOfHoverboards -= 1\r\nconsole.log ( "There are at least " + numberOfHoverboards + " hoverboard(s) in 2015");\r\n```	\N	\N	15
111	```javascript\r\nvar number_of_hoverboards = "1";\r\nconsole.log("There are at least " + number_of_hoverboards + " hoverboard(s) in 2015.");\r\nparseInt(number_of_hoverboards);\r\nnumber_of_hoverboards -= 1;\r\nconsole.log("There are at least " + number_of_hoverboards + " hoverboard(s) in 2015.");\r\n```	\N	\N	15
112	```javascript\nvar numberOfHoverboards = "1";\nconsole.log ("There are at least "+numberOfHoverboards+"  hoverboard(s) in 2015.");\nvar numberOfHoverboards = parseInt("1");\nvar numberOfHoverboards = 1;\nconsole.log ("There are at least "+numberOfHoverboards+"  hoverboard(s) in 2015.");\n```\n\n	\N	\N	15
113	```javascript\nvar numberOfHoverboards = "1";\nconsole.log("There are at least", numberOfHoverboards, "hoverboard(s) in 2015.");\nnumberOfHoverboards = parseInt("1");\nnumberOfHoverboards -= 1;\nconsole.log("There are at least", numberOfHoverboards, "hoverboard(s) in 2015.");\n```	\N	\N	15
114	```javascript\r\n\r\nvar number_of_hoverboards = "1";\r\nconsole.log( "There are at least " +number_of_hoverboards + "  hoverboard(s) in 2015.");\r\n var number_of_hoverboards = parseFloat(number_of_hoverboards);\r\n\r\n\r\nconsole.log("There are at least " + number_of_hoverboards +  " hoverboard(s) in 2015.");\r\n\r\n\r\n\r\n```	\N	\N	15
115	```javascript\r\nvar number_of_hoverboards = "1";\r\nconsole.log("There are at least # " +number_of_hoverboards+ " hoverboard(s) in 2015.");\r\n\r\nvar number_of_hoverboards =Number(number_of_hoverboards);\r\nvar number_of_hoverboards = number_of_hoverboards+1;\r\nconsole.log("There are at least # " +number_of_hoverboards+ " hoverboard(s) in 2015.");\r\n```	\N	\N	15
116	```javascript\nvar numberOfHoverboards = "1";\nconsole.log("There are at least # " +numberOfHoverboards+ " hoverboard(s) in 2015.");\n\nvar numberOfHoverboards = Number(numberOfHoverboards);\nvar numberOfHoverboards = numberOfHoverboards  -=  1;\nconsole.log("There are at least # " +numberOfHoverboards+ " hoverboard(s) in 2015.");\n```	\N	\N	15
117	```javascript\r\n\r\n\r\n\r\nvar hoverboards = "1"\r\nconsole.log("There are at least " + hoverboards + " hoverboard(s) in 2015.")\r\n\r\n hoverboards -= "1"\r\nconsole.log("There are at least " + hoverboards + " hoverboard(s) in 2015.")\r\n```	\N	\N	15
71	```js\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\nfor (var i in a){\r\n  console.log(i, a[i]);\r\n}\r\n```	test	14	14
72	```javascript\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\nfor (var i in a) {\n  if (a.hasOwnProperty(i)) {\n    console.log(i, a[i]);\n  }\n}\n```	test	15	14
73	```js\r\n\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\nfor (i in a) {\r\n  console.log(i, ":", a[i]);\r\n}\r\n```	training	14	14
74	```javascript\r\n\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\nfor (i in a) {\r\n  console.log(i , a[i]);\r\n}\r\n\r\n```	training	14	14
75	```javascript\n[a].forEach(\n    function(pair){\n      console.log(a)\n    });\n```	training	16	14
76	```javascript\r\n\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\nfor (var key in a ){\r\n  console.log(key + ': ' + a[key]);\r\n}\r\n\r\n```	training	14	14
78	```javascript\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\nfor (var i in a){\r\n  console.log(i, a[i]);\r\n}\r\n```	training	14	14
79	```javascript\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\nObject.keys(a).forEach(function(key, value) {\r\n        console.log(key, value);\r\n    });\r\n\r\n```	training	16	14
80	```js\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\nfor (var key in a) \r\n{\r\n    if (a.hasOwnProperty(key))\r\n    {\r\n    console.log(key + " = " + a[key]);\r\n    }\r\n}\r\n```	training	15	14
81	```javascript\nfor (var i in a) {\n  console.log(i, a[i]);\n}\n```	training	17	14
82	```js\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\n\r\nfor (var key in a ) {\r\n  console.log(key+':', a[key]);\r\n}\r\n```	training	14	14
83	```javascript\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\nfor (var i in a) {\n  console.log((i) + ': ' + a[i]);\n}\n```	training	14	14
85	```javascript\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 }; \r\nfor(var propt in a) {\r\nconsole.log(propt + ': ' + a[propt]);\r\n}\r\n```	training	14	14
88	```js\r\n\r\nvar a = { one: 1, two: 2, three: 3, four: 4, five: 5 };\r\n\r\n\r\n\r\n\r\nfor (var key in a) {\r\n  if (a.hasOwnProperty(key)) {\r\n    console.log(key + " : " + a[key]);\r\n  }\r\n}\r\n\r\n\r\n```	training	15	14
64	`-1 + 1`\n`!true && !false`\n`1 - 1`\n`!!true or !false`	training	12	9
65	```ruby\n-1 + 1\n!true && !false\n1 - 1\n!!true || !false\n```	training	11	9
55	-1+1\r\nnot true and not false\r\n1-1\r\n!!true or !false\r\n	training	13	9
56	```ruby\r\n-(1 - 1) == -1+1\r\n\r\nnot(true or false) == false and true\r\n\r\n-(-1+1) == 1-1\r\n\r\nnot(!true and false) == true or false\r\n\r\n```	training	11	9
94	```javascript\r\n\r\nvar numberOfHoverboards = "1"\r\nconsole.log("There are at least " + numberOfHoverboards + " hoverboard(s) in 2015.");\r\nvar numberOfHoverboards = parseInt(numberOfHoverboards);\r\nnumberOfHoverboards -= 1\r\n\r\nconsole.log("There are at least " + numberOfHoverboards + " hoverboard(s) in 2015.");\r\n```	\N	\N	15
95	```js\r\n\r\nvar number_of_hoverboards = “1”;\r\nconsole.log("There are at least “ + number_of_hoverboards + “hoverboard(s) in 2015.”\r\n);\r\n\r\nvar n = num.toString();\r\nvar int = number_of_hoverboards.tostring();\r\nint -= 1;\r\n\r\nconsole.log("There are at least” + int + “ hoverboard(s) in 2015.”);\r\n\r\n```	\N	\N	15
96	```javascript\nvar number_of_hoverboards = "1";\nconsole.log("There are at least " + number_of_hoverboards + " hoverboard(s) in 2015.");\nnumber_of_hoverboards -= 1; // now = 0\n\nconsole.log("There are at least " + number_of_hoverboards + " hoverboard(s) in 2015.");\n```	\N	\N	15
97	```javascript\nvar numberOfHoverboards = "1";\nconsole.log("There are at least" + numberOfHoverboards + " hoverboard(s) in 2015.");\nnumberOfHoverboards = parseInt(numberOfHoverboards);\nnumberOfHoverboards -= 1;\n\nconsole.log("There are at least" + numberOfHoverboards+ " hoverboard(s) in 2015.");\n```	\N	\N	15
54	-1+1\r\nnot true and not false\r\n1-1\r\nnot !true or not false	training	\N	9
66	```ruby\r\n-(1-1) == -1 +1\r\nnot(true or false) == false or true\r\n-(-1 + 1) == 1 -1\r\nnot(!true and false) == true and true\r\n```	training	\N	9
67	`-1 +1`  \r\n`(not true) and (not false)`  false  \r\n`+1 -1`  \r\n`(not !true) or (not false)`  true	training	\N	9
68	`-(1 - 1)` == `-1 + 1`\r\n`not(true or false)` == `false and true` \r\n`puts -(-1+1)` == `(1 - 1)`\r\n`puts not(!true and false)` == `not(false and false)`	training	\N	9
69	```ruby\n-1 + 1\n!true and !false\n1 - 1\n!!true or !false\n```	training	\N	9
70	```ruby\n- 1 + 1  \nnot true and not false  \n 1 - 1  \n true or true  \n```	training	\N	9
98	```js\r\nfunction puts(arg) {\r\n\tconsole.log(arg);\r\n}\r\n\r\nvar number_of_hoverboards = "1";\r\n\r\nputs("There are at least " + number_of_hoverboards +" hoverboard(s) in 2015.");\r\n\r\nnumber_of_hoverboards = parseInt(number_of_hoverboards);\r\n\r\nnumber_of_hoverboards -= 1;\r\n\r\nputs("There are at least " + number_of_hoverboards +" hoverboard(s) in 2015.");\r\n```	\N	\N	15
99	```js\nvar number_of_hoverboards = parseInt("1", 1);\nvar hoverboard_sentence = "There are at least " + number_of_hoverboards + " hoverboard(s) in 2015."; \n  console.log(hoverboard_sentence);\n\n\nvar number_of_hoverboards -== 1; \n  console.log(hoverboard_sentence);\n```	\N	\N	15
100	```javascript\nvar numberOfHoverboards = "1"\nconsole.log("There are at least", numberOfHoverboards, "hoverboard(s) in 2015");\nnumberOfHoverboards = parseInt("1")\nnumberOfHoverboards -= 1\nconsole.log("There are at least", numberOfHoverboards,  "hoverboard(s) in 2015");\n```	\N	\N	15
101	```js\r\n\r\nvar number_of_hoverboards = "1";\r\nconsole.log("There are at least " + number_of_hoverboards + " hoverboard(s) in 2015.");\r\nvar number_of_hoverboards = parseInt(number_of_hoverboards);\r\nnumber_of_hoverboards -= 1;\r\nconsole.log("There are at least " + number_of_hoverboards + " hoverboard(s) in 2015.");\r\n\r\n```	\N	\N	15
102	```javascript\r\n\r\nvar number_of_hoverboards = "1";\r\nvar output = "There are at least " + number_of_hoverboards + " hoverboard(s) in 2015";\r\nconsole.log(output)\r\nparseInt(number_of_hoverboards)\r\nvar number_of_hoverboards_new = number_of_hoverboards - 1\r\nvar output2 = "There are at least " + number_of_hoverboards_new + " hoverboard(s) in 2015";\r\nconsole.log(output2)\r\n\r\n\r\n```	\N	\N	15
103	```javascript\r\nvar numberOfHoverboards = "1";\r\nconsole.log("There are at least " + numberOfHoverboards + " hoverboard(s) in 2015.");\r\nnumberOfHoverboards -= 1;\r\nconsole.log("There are at least " + numberOfHoverboards + " hoverboard(s) in 2015.");\r\n```	\N	\N	15
104	```js\nvar number_of_hoverboards = "1"\n  console.log("There are at least " + number_of_hoverboards + " hoverboard(s) in 2015.");\nvar number_of_hoverboards2 = (number_of_hoverboards--)\n  console.log("There are at least " + number_of_hoverboards + " hoverboard(s) in 2015.")\n```	\N	\N	15
105	```javascript\r\nvar numberOfHoverboards = "1";\r\nconsole.log( "There are at least " + numberOfHoverboards + " hoverboard(s) in 2015.");\r\nnumberOfHoverboards = Number(numberOfHoverboards);\r\nnumberOfHoverboards -= 1;\r\n\r\nconsole.log("There are at least " + numberOfHoverboards + " hoverboard(s) in 2015.");\r\n```	\N	\N	15
106	```javascript\nvar numberOfHoverboards = "1";\nconsole.log("There are at least " + numberOfHoverboards + " hoverboard(s) in 2015.");\nnumberOfHoverboards = parseInt(numberOfHoverboards);\n\nnumberOfHoverboards -= 1;\nconsole.log("There are at least " + numberOfHoverboards + " hoverboard(s) in 2015.")\n```	\N	\N	15
107	```javascript\r\n\r\nvar hoverboard_number = parseInt("1");\r\nvar hoverboard_number2 = hoverboard_number--;\r\nconsole.log("There are at least" + " " + hoverboard_number2 + " " + " hoverboard(s) in 2015")\r\nconsole.log("There are at least" + " " + hoverboard_number + " " + " hoverboard(s) in 2015")\r\n\r\n```	\N	\N	15
118	```javascript\r\nvar numberOfHoverboards = "1"\r\nconsole.log("There are at least", numberOfHoverboards, "hoverboard(s) in 2015");\r\nnumberOfHoverboards = parseInt("1")\r\nnumberOfHoverboards -= 1\r\nconsole.log("There are at least", numberOfHoverboards,  "hoverboard(s) in 2015");\r\n```	\N	\N	15
57	```ruby\r\n-(1 - 1) == -1 + 1 == 0\r\nnot(true or false) == not true and not false == false and true == false\r\n-(-1+1) == 1 - 1 == 0\r\nnot(!true and false) == not !true or not false == not false or not false == true or true == true\r\n```	training	11	9
58	-1 - 1\r\n1+1	training	12	9
59	- (1 - 1) == -1 + 1\r\nnot (true or false) == false and true\r\n-(-1 + 1) == 1 - 1\r\nnot (!true and false) == true or true \r\n	training	13	9
60	```ruby\r\n-(1 - 1) == -1 + 1\r\nnot(true or false) == not true and not false\r\n-(-1+1) == 1 - 1\r\nnot(!true and false) == not true or not false\r\n```	training	11	9
61	-1 + 1  \r\nfalse || true  \r\n1 - 1  \r\ntrue && true\r\n	training	13	9
62	-1 -(-1)\r\n!true and !false\r\n-(-1) -1\r\nnot(!true) or not false	training	13	9
63	-1 + 1\r\nnot true and  not false\r\n1 + -1\r\n!!true or !false	training	13	9
\.


--
-- Name: responses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: whoisjose04
--

SELECT pg_catalog.setval('responses_id_seq', 118, true);


--
-- Data for Name: units; Type: TABLE DATA; Schema: public; Owner: whoisjose04
--

COPY units (id, title, description) FROM stdin;
\.


--
-- Name: units_id_seq; Type: SEQUENCE SET; Schema: public; Owner: whoisjose04
--

SELECT pg_catalog.setval('units_id_seq', 1, false);


--
-- Name: categories_pkey; Type: CONSTRAINT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: questions_pkey; Type: CONSTRAINT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- Name: responses_pkey; Type: CONSTRAINT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY responses
    ADD CONSTRAINT responses_pkey PRIMARY KEY (id);


--
-- Name: units_pkey; Type: CONSTRAINT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY units
    ADD CONSTRAINT units_pkey PRIMARY KEY (id);


--
-- Name: categories_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY categories
    ADD CONSTRAINT categories_question_id_fkey FOREIGN KEY (question_id) REFERENCES questions(id);


--
-- Name: questions_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY questions
    ADD CONSTRAINT questions_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES units(id);


--
-- Name: responses_categories_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY responses
    ADD CONSTRAINT responses_categories_id_fkey FOREIGN KEY (categories_id) REFERENCES categories(id);


--
-- Name: responses_questions_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: whoisjose04
--

ALTER TABLE ONLY responses
    ADD CONSTRAINT responses_questions_id_fkey FOREIGN KEY (questions_id) REFERENCES questions(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: whoisjose04
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM whoisjose04;
GRANT ALL ON SCHEMA public TO whoisjose04;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

