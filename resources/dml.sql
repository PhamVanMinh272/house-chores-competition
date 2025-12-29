-- seed.sql

-- Users
INSERT INTO t_user (name) VALUES
('Minh'),
('Đạt'),
('Thiên'),
('Tâm'),
('Tấn'),
('Thoại'),
('Giao'),
('Ân');

-- Groups
INSERT INTO t_group (name) VALUES
('La Palace'),
('Household B');

-- Members (users assigned to groups)
INSERT INTO t_member (group_id, user_id, member_nickname) VALUES
(1, 1, 'Minh A'),
(1, 2, 'Đạt A'),
(2, 3, 'Thiên A'),
(2, 4, 'Tâm A'),
(2, 5, 'Tấn B'),
(2, 6, 'Thoại B'),
(2, 7, 'Giao B'),
(2, 8, 'Ân B');

-- Chores
INSERT INTO t_chore (name, point, group_id) VALUES
('Wash dishes', 10, 1),
('Vacuum floor', 15, 1),
('Take out trash', 5, 1),
('Cook dinner', 20, 2),
('Laundry', 15, 2),
('Clean bathroom', 25, 2);

-- Schedules (assign chores to members on dates)
INSERT INTO t_schedule (schedule_date, chore_id, member_id, point, status, comment) VALUES
('2025-12-29', 1, 1, 10, 'Pending', 'Evening shift'),
('2025-01-01', 2, 2, 15, 'InProgress', 'Started vacuuming'),
('2025-01-02', 3, 3, 5, 'Done', 'Trash taken out'),
('2025-01-02', 4, 5, 20, 'Pending', 'Dinner prep'),
('2025-01-03', 5, 6, 15, 'Done', 'Laundry finished'),
('2025-01-03', 6, 7, 25, 'FullyReviewed', 'Bathroom spotless'),
('2025-01-04', 1, 4, 10, 'Pending', 'Morning dishes'),
('2025-01-04', 2, 8, 15, 'Pending', 'Vacuum before guests');