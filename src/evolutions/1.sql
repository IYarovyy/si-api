-- Departments -------------------------------------------------------
DROP TABLE IF EXISTS departments;
CREATE TABLE departments (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    parent integer,
    dname varchar(255) not null
);

CREATE INDEX departments_parent ON departments(parent int4_ops);

-- Roles -------------------------------------------------------
DROP TYPE IF EXISTS user_role CASCADE;
CREATE TYPE user_role AS ENUM ('chief', 'regular', 'operator');

-- Users -------------------------------------------------------
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department integer,
    urole user_role not null,
    first_name varchar(255),
	  second_name varchar(255),
	  email varchar(255) not null,
	  password varchar(255)
);

CREATE INDEX users_department ON users(department int4_ops);

-- Tasks -------------------------------------------------------
DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_by integer,
    in_work BOOLEAN,
    -- ADD REQUIRED FIELDS --
    tname varchar(255) not null
);

CREATE INDEX tasks_creator ON tasks(created_by int4_ops);

-- Subtasks -------------------------------------------------------
DROP TABLE IF EXISTS subtasks;
CREATE TABLE subtasks (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    parent integer,
    assigned_to integer,
    -- ADD REQUIRED FIELDS --
    tname varchar(255) not null
);

CREATE INDEX subtasks_parent ON subtasks(parent int4_ops);
CREATE INDEX subtasks_assigned ON subtasks(assigned_to int4_ops);

-- Function -----------------------------------------------------
create or replace function subordinates(dep integer)
  returns table (id integer, parent integer, dname text)
as
$body$
	WITH RECURSIVE dep_hierarchy AS (
	  SELECT id, parent, dname
	  FROM departments
	  WHERE id=$1

	  UNION ALL

	  SELECT    departments.id,
	            departments.parent,
	            departments.dname
	  FROM departments, dep_hierarchy
	  WHERE departments.parent = dep_hierarchy.id
	)
	SELECT *
	FROM dep_hierarchy;
$body$
language sql;