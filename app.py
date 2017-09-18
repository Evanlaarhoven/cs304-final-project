#!/usr/local/bin/python2.7

## Emily Van Laarhoven and Marissa Okoli
## app.py
## Last modified: 5/12/2017
## driver for web pages and forms

from flask import Flask, render_template, flash, request, redirect, url_for, make_response
import os
import db_curs
import db_acct
import db_job
import showJobs
import acceptJob
import db_review
import db_viewAcct
import db_allAccts
import deleteJob

app = Flask(__name__)
app.secret_key = "asgaoihrnasdfkjd" #secret key needed for flashing

DATABASE = "oddjobs_db"

@app.route('/')
def home():
    return render_template("base.html", page_title="OddJobs Home")

@app.route('/create_account/',methods=['POST','GET'])
def create_account():
## '''inserts data from form into account table'''
    if request.method=="POST":
        cursor = db_curs.cursor()
        skills = request.form.getlist('skills')
        if db_acct.create_account(cursor,request.form,skills):
            flash("account has been created successfully")
        else:
            flash("something went wrong")
    return render_template("create_account.html",page_title="Create Account")

@app.route('/create_job/',methods=['POST','GET'])
def create_job():
## '''inserts data from form into job table'''
    if request.method=="POST":
        cursor = db_curs.cursor()
        if db_job.create_job(cursor,request.form):
            flash("job has been created successfully")
        else:
            flash("something went wrong")
    return render_template("create_job.html",page_title="Post a New Job")
    
@app.route('/setcookie',methods = ['POST','GET'])
def setcookie():
## '''sets the zipcode cookie when user searches'''
    if request.method == 'POST':
        zipcode = request.form['zipcode']
        cursor = db_curs.cursor()
        jobList = showJobs.getJobs(cursor,zipcode)
        zipDict = {'zipcode':str(zipcode) }
        response = make_response(render_template('joblistings.html', allCookies=zipDict, jobs=jobList))
        response.set_cookie('zipcode',zipcode)
        return response

@app.route('/view_jobs/',methods=['POST','GET'])
def view_jobs():
## '''displays list of jobs and allows user to accept or delete job'''
    if request.method=="POST":
	uid = request.form['userId']
	jid = request.form['jid']
        if request.form['btn'] == "Submit":
             if int(uid) == 0:
                 flash("only enter 0 to confirm a deletion")
             elif acceptJob.main(uid, jid):
                 flash("Job accepted")
                 return redirect(url_for('home'))
             else:
                 flash("Error occurred - submit")
        if request.form['btn'] == "Delete":
             if int(uid) != 0:
                 flash("enter 0 for uid to confirm deletion")
             elif deleteJob.main(uid, jid):
                 flash("Job deleted")
             else:
                 flash("Error occured - delete")
    cursor = db_curs.cursor()
    zipcode = request.cookies.get('zipcode')
    if zipcode == "":
        zipcode == None
    jobList = showJobs.getJobs(cursor,zipcode)
    return render_template("joblistings.html",allCookies=request.cookies, jobs=jobList)


@app.route('/review/',methods=['POST','GET'])
def review():
## '''allows both employees and employers to review, link from account page''' 
	if request.method=="POST":
            cursor = db_curs.cursor()
            if db_review.insert_review(cursor,request.form):
                flash("review submitted")
            else:
                flash("something went wrong")
        return render_template("review.html",page_title="Leave a Review")


@app.route('/view_account/<uid>',methods=['POST','GET'])
def view_account(uid):
## '''used to look at individual user profile, linked form search page'''
    cursor = db_curs.cursor()
    if db_viewAcct.isActive(cursor,uid):
        if request.method == "POST":
            if  db_acct.deleteAcct(cursor,uid):
                flash("You have successfully deleted your account")
                return redirect(url_for('home'))
        acct_info = db_viewAcct.search_uid(cursor,uid) 
        return render_template("view_account.html",acct_info=acct_info)
    else:
        flash("this account was deleted")
        return redirect(url_for('home'))

@app.route('/search_account/',methods=['POST','GET'])
def search_account():
## '''links to individual account pages'''
    cursor = db_curs.cursor()
    if request.method == "POST":
        return redirect(url_for('view_account',uid=request.form['uid']))
    all_accounts = db_allAccts.list_users(cursor)
    return render_template("search_account.html",all_accounts=all_accounts)

if __name__=='__main__':
    app.debug = True
##    app.run('0.0.0.0',os.getuid()) ## Marissa and I work on different projects
    app.run('0.0.0.0',6849)
