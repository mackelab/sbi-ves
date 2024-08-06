create table if not exists "user"
(
    id          uuid primary key,
    first_name  varchar(255) not null,
    last_name   varchar(255) not null,
    institution varchar(255) null,
    username    varchar(255) not null,
    password    varchar(255) not null,
    email       varchar(255) not null,
    created_at  timestamp default current_timestamp
);

create table if not exists measurement
(
    id               uuid primary key,
    user_id          uuid         not null,
    file_id          uuid         not null,
    ab2_2            float        null,
    ab2_2_5          float        null,
    ab2_3            float        null,
    ab2_3_6          float        null,
    ab2_4_4          float        null,
    ab2_5_2          float        null,
    ab2_6_3          float        null,
    ab2_7_5          float        null,
    ab2_8_7          float        null,
    ab2_10           float        null,
    ab2_12           float        null,
    ab2_14_5         float        null,
    ab2_17_5         float        null,
    ab2_21           float        null,
    ab2_25           float        null,
    ab2_30           float        null,
    ab2_36           float        null,
    ab2_44           float        null,
    ab2_52           float        null,
    ab2_63           float        null,
    ab2_75           float        null,
    ab2_87           float        null,
    ab2_100          float        null,
    location         varchar(255) null,
    measurement_date date         null,
    comment          varchar(255) null,
    created_at       timestamp default current_timestamp,
    foreign key (user_id) references "user" (id),
    foreign key (file_id) references "file" (id)
);

create table if not exists "file"
(
    id             uuid primary key,
    user_id        uuid         not null,
    file_name      varchar(255) not null,
    file_extension varchar(255) not null,
    file_size      varchar(255) not null,
    created_at     timestamp default current_timestamp,
    foreign key (user_id) references "user" (id)
);