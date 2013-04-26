#!/user/bin/python

import os,re
from python.autoRegression_pusher import * 

database = "fwmrm_oltp_jmo" #replace with ur own database
home_dir = "/home/jmo"      #replace with ur regression Upper-level directory. 

regression_dir = home_dir + "/regression"
tmp_regression_dir = "/tmp/regression"
sql_dir = regression_dir + "/sql"
cxml_dir = regression_dir + "/requestxml"
bxml_dir = regression_dir + "/brequests"
python_dir = regression_dir + "/python"

def clone_file(cpfile, todir):
    if os.path.isfile(cpfile):
        os.system("cp %s %s" % (cpfile, todir))
        print "file %s has been cloned to dir: %s" % (cpfile, todir)
    else: print "No file exists for %s" % cpfile 

def clone_regression():
    #os.system("rsync -av --exclude=.svn --exclude=.log %s %s" % (tmp_regression_dir, home_dir))
    os.system("rsync -av --include '*.sql' --include '*.xml' --include '*.txt' --exclude '*.log' --exclude '.svn' %s %s" % (tmp_regression_dir, home_dir))

    if os.path.isfile(regression_dir + "/readme.txt"):
        print "Success in regression clone to dir: " + regression_dir  + "."

def replace_database():
    for root, dirs, files in os.walk(sql_dir):
        for name in files:
            if (os.path.splitext(name)[1] in [".sql"]) : 
                stream = open( sql_dir + "/" + name).read()
                f = open( sql_dir + "/" + name, "w")
                f.write( re.sub("fwmrm_oltp",database,stream))
                f.close()
    print "Success in switch to database: " + database

def replace_script_dir():
    for root, dirs, files in os.walk(python_dir):
        for name in files:
            if(os.path.splitext(name)[1] in [".py"]):
                stream = open( python_dir + "/" + name).read()
                f = open( python_dir + "/" + name, "w")
                f.write( re.sub("/regression/regression/regression", regression_dir, stream))
                f.close()
    
    print "Success in python script dirs replacement."

def mkdir_result():
    if(not os.path.isdir(regression_dir + "/result")):
        os.system("mkdir %s" % (regression_dir + "/result"))
    print "Success in mkdir " + regression_dir + "/result"

if __name__ == '__main__':
    _mode = "pusher"
    _case_id = ""
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:',[])
    except:
        print __doc__
        sys.exit(-1)

    for opt, arg in opts:
        if opt=='-c': _case_id = arg
    
    if not _case_id:
        clone_regression()
        replace_database()
        replace_script_dir()
        mkdir_result()


    autoTest = AutoRegression(_mode, _case_id, branch='debug')
    caseids = autoTest.cases.getAllCase().keys()
    
    if _case_id in caseids:
        baseURL, cxmls, bxmls = autoTest.getPrepareCaseInfo(_case_id)
        basesql  = autoTest.cases.getAllCase()[_case_id][3]
        sendsql  = autoTest.cases.getAllCase()[_case_id][4]
        
        tmp_base_sql = tmp_regression_dir + "/sql/" + basesql.strip()
        tmp_send_sql = tmp_regression_dir + "/sql/" + sendsql.strip()
        clone_file(tmp_base_sql, sql_dir)
        clone_file(tmp_send_sql, sql_dir)

        for cxml in cxmls:
            tmp_cxml = tmp_regression_dir + "/requestxml/" + cxml.strip()
            clone_file(tmp_cxml, cxml_dir)
        
        for bxml in bxmls:
            tmp_bxml = tmp_regression_dir + "/brequests/" + bxml.strip()
            clone_file(tmp_bxml, bxml_dir)
    else:
       print "case id [%s] does not exist." % _case_id

    
    
