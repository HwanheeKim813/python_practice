# Write your code here

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Sequence

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def menu():
    while 1:
        print('1) Today\'s tasks')
        print('2) Week\'s tasks')
        print('3) All tasks')
        print('4) Missed tasks')
        print('5) Add task')
        print('6) Delete task')
        print('0) Exit')
        a = int(input())
        if a == 1:
            today = datetime.today()
            print('Today {date}:'.format(date=today.strftime('%d %b')))
            todo()
        elif a == 2:
            week_list()
        elif a == 3:
            all_task()
        elif a == 4:
            missed_task()
        elif a == 5:
            add_list()
        elif a == 6:
            delete_list()
        elif a == 0:
            print('Bye!')
            try:
                session.query(Task).delete()
                session.commit()
            except:
                session.rollback()
            session.close()
            engine.dispose()
            break
        print('')


def todo(day=datetime.today().date()):
    num = 0
    rows = session.query(Task).filter(Task.deadline == day).all()
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for i in rows:
            num += 1
            print('{0}. {1}'.format(num, i))
    print('')
    session.commit()


def add_list():
    tasks = input('Enter task')
    date_string = input('Enter deadline')
    day = datetime.strptime(date_string, '%Y-%m-%d')
    new_row = Task(task=tasks, deadline=day.date())
    session.add(new_row)
    session.commit()
    print('The task has been added!')


def week_list():
    today = datetime.today().date()
    for i in range(7):
        day = today + timedelta(days=i)
        print('{date}:'.format(date=day.strftime('%A %d %b')))
        todo(day)


def all_task():
    num = 0
    rows = session.query(Task).all()
    print('All tasks:')
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for i in sorted(rows):
            num += 1
            print('{0}) {1}'.format(num, i))
    session.commit()


def delete_list():
    list_dic = {}
    num = 0
    rows = session.query(Task.task, Task.id).all()
    print('Chose the number of the task you want to delete:')
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for i in rows:
            num += 1
            list_dic[num] = i.id
            print('{0}) {1}'.format(num, i.task))
    n = int(input())
    session.query(Task).filter(Task.id == list_dic[n]).delete()
    session.commit()
    print('The task has been deleted!')


def missed_task():
    num = 0
    rows = session.query(Task).filter(Task.deadline < datetime.today().date()).all()
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for i in rows:
            num += 1
            print('{0}. {1}.'.format(num, i))
    print('')
    session.commit()


menu()
