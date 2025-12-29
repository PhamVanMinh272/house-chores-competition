-- schema.sql

-- Users table
CREATE TABLE t_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Groups table
CREATE TABLE t_group (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Members table: links users to groups
CREATE TABLE t_member (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    member_nickname TEXT,
    FOREIGN KEY (group_id) REFERENCES t_Group(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES t_User(id) ON DELETE CASCADE
);

-- Chores table: belongs to a group
CREATE TABLE t_chore (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    point INTEGER NOT NULL DEFAULT 0,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES t_Group(id) ON DELETE CASCADE
);

-- Schedule table: assigns a chore to a member on a date
CREATE TABLE t_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    schedule_date DATE NOT NULL,
    chore_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    point INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL CHECK (status IN ('Pending','InProgress','Done','FullyReviewed')),
    comment TEXT,
    FOREIGN KEY (chore_id) REFERENCES t_Chore(id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES t_Member(id) ON DELETE CASCADE
);