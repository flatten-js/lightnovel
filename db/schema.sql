drop table if exists triplet_freqs;
create table triplet_freqs(
  id integer primary key autoincrement not null,
  prefix1 text not null,
  prefix2 text not null,
  suffix text not null,
  freq integer not null
);
