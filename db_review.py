## Emily Van Laarhoven 
## db_review.py
## Last modified: 5/10/2017
## Insert review into rating table in db

import dbconn2
import MySQLdb
import os
from oddjobs_dsn import DSN

## global variables
DATABASE = 'oddjobs_db'
DEBUG = False

def insert_review(cursor,form_info):
    '''inserts a review into rating table'''
    jid = form_info['jid']
    me = form_info['myId']
    them = form_info['theirId']
    rating = form_info['rating']
    comment = form_info['review_comments']
    who = form_info['who']
    if who=="employee": #if employee is leaving employer review
        q2 = "select employer_rating from rating where jid=%s and employee_id=%s;"
        if update_review(cursor,jid): #if employer has already reviewed for that job
            q1 = "update rating set jid=%s, employee_id=%s, employer_id=%s, employer_rating=%s, employer_review=%s where jid=%s;"
            inputs = [jid,me,them,rating,comment,jid]
        else: #if employee is the first to review for that job
            q1 = "Insert into rating (jid,employee_id,employer_id,employer_rating,employer_review) values (%s,%s,%s,%s,%s);"
            inputs = [jid,me,them,rating,comment]
    if who=="employer": #if employer is leaving a review of employee
        q2 = "select employee_rating from rating where jid=%s and employer_id=%s;"
        if update_review(cursor,jid): #if employee has already left a review then update
            q1 = "update rating set jid=%s, employer_id=%s, employee_id=%s, employee_rating=%s, employee_review=%s where jid=%s;"
            inputs = [jid,me,them,rating,comment,jid]
        else: #if employer is first to review for that job
            q1 = "Insert into rating (jid,employer_id,employee_id,employee_rating,employee_review) values (%s,%s,%s,%s,%s);"        
            inputs = [jid,me,them,rating,comment]    
    cursor.execute(q1,inputs)
    #check if insertion was successful and return boolean
    cursor.execute(q2,[jid,me])
    if who =="employee":
        return cursor.fetchone()['employer_rating'] != "NULL"
    if who =="employer":
        return cursor.fetchone()['employee_rating'] != "NULL"

def update_review(cursor,jid):
    '''helper method returns true if there is already a row for that jid'''
    q = "select count(*) from rating where jid=%s;"
    cursor.execute(q,[jid])
    val = cursor.fetchone()['count(*)']
    return val > 0
