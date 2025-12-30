- I want to make a website to manage house chores. View house chores need to be done daily or weekly. Mark status, done by. Count point for who has done the house chores.
 
User can create house chores (name, description, point)
User can update the house chores.
User can see a list of all house chores.
User can pick house chores to any day.
Show calendar and see list house chore for the day.
 
 
t_User(id, name)
t_Group(id, name)
t_Member (id, group_id, user_id, nickname)
 
t_chore (id, name, point, group_id)
 
t_Schedule (id, schedule_date, chore_id, member_id, point, status, comment) # status: Pending, InProgress, Done, FullyReviewed
 
 
v_Point(id, member_id, schedule_date, period, total_point, status) # period: daily, weekly, monthly
 
 
Show list house chores of a group:
select id, name, point from t_chore
where group_id = <group_id>
 
Show all schedule for a group:
 
select id, date, chore_id, user_id, point, status, comment
from t_Schedule
join t_chore on t_Schedule.chore_id = t_chore.id
where group_id=<group_id> and date between <start_date> and <end_date>
 
Show member point:
 
select user_id, nickname, point as total_point
from t_Schedule
join t_member on t_member.id = t_Schedule.member_id
where t_member.group_id=<group_id> and date between <start_date> and <end_date>
group by user_id, nickname
 
Show list of member in a group:
select user_id, nickname, t_user.name
from t_member
join t_user on t_user.id = t_member.user_id
 
 
Show list of groups of a user:
select t_group.id, t_group.name
from t_group
join t_member on t_group.id = t_member.group_id
where t_member.user_id = <user_id>