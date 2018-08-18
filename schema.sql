CREATE USER packer_autobuild;
CREATE DATABASE packer_autobuild OWNER packer_autobuild;
\connect packer_autobuild;


CREATE TABLE runner_groups (
	group_id bigserial primary key,
	group_name text NOT NULL UNIQUE,
	note text
);
ALTER TABLE runner_groups OWNER TO packer_autobuild;

CREATE TABLE runners (
	runner_id bigserial primary key,
	host_name text NOT NULL UNIQUE,
	group_name text references runner_groups(group_name)
);
ALTER TABLE runners OWNER TO packer_autobuild;

CREATE TABLE local_users (
	user_id bigserial primary key,
	username text UNIQUE,
	email text UNIQUE,
	password text NOT NULL
);
ALTER TABLE local_users OWNER TO packer_autobuild;


CREATE TABLE local_user_groups (
	group_id bigserial primary key,
	group_name text UNIQUE NOT NULL
);
ALTER TABLE local_user_groups OWNER TO packer_autobuild;


CREATE TABLE users_groups_map (
	id bigserial primary key,
	user_id bigserial references local_users(user_id),
	group_id bigserial references local_user_groups(group_id)
);
ALTER TABLE users_groups_map OWNER TO packer_autobuild;

CREATE TABLE repos (
	repo_id bigserial primary key,
	repo_url text NOT NULL,
	repo_name text NOT NULL,
	branch text NOT NULL,
	UNIQUE (branch, repo_url)
);
ALTER TABLE repos OWNER TO packer_autobuild;

CREATE TABLE jobs (
	job_id bigserial primary key,
	finished boolean,
	log text,
	schedule text NOT NULL,
	repo_id bigserial references repos(repo_id),
	username text,
	started timestamp,
	completed timestamp
);
ALTER TABLE jobs OWNER TO packer_autobuild;

INSERT INTO runner_groups (group_name, note) values ('default_group','default group');