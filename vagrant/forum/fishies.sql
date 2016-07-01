$ psql
=> create database fishies;
=> \c fishies
=> create table fish(content text, id serial primary key);
=> insert into fish values('some text content');