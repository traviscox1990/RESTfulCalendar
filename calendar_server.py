#!flask/scripts/python
from flask import Flask, jsonify, abort, request, make_response, url_for
 
app = Flask(__name__, static_url_path = "")
  
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request 400' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found 404' } ), 404)


class Calendar(object):
    _registry = []
    def __init__(self,user_id):
        self._registry.append(self)
        self.UserTag = user_id
        
        self.Mon = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        self.Tues = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        self.Wed = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        self.Thur =[ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        self.Fri = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        self.Sat = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        self.Sun = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        self.FullCal = [self.Mon,\
                        self.Tues,\
                        self.Wed,\
                        self.Thur,\
                        self.Fri,\
                        self.Sat,\
                        self.Sun]
    def erase(self):
        self._registry.remove(self)
    def resetDay(self,day):
        if day.lower() == "monday":
           self.Mon = [ {str(i+1)+" o'clock": "" } for i in range(0,24)] 
        if day.lower() == "tuesday":
            self.Tues = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        if day.lower() == "wednesday":
            self.Wed = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        if day.lower() == "thursday":
            self.Thur = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        if day.lower() == "friday":
            self.Fri = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        if day.lower() == "saturday":
            self.Sat = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        if day.lower() == "sunday":
            self.Sun = [ {str(i+1)+" o'clock": "" } for i in range(0,24)]
        
    

@app.route('/calendar/api/v1.0/<int:password>', methods = ['LOU'])

def ListOfUsers(password):
    if password == 12345:
        l = [i.UserTag for i in Calendar._registry]
    else:
        abort(400)
    return jsonify( { "Users" : l } )


@app.route('/calendar/api/v1.0/<user_tag>', methods = ['MNC'])

def MakeNewCalendar(user_tag):
    calendar1 = ""
    for p in Calendar._registry:
        if p.UserTag == user_tag:
            return jsonify( {user_tag:"This User Handle already exists"} )
    cal = Calendar(user_tag)
    s = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    Cal = [cal.Mon,cal.Tues,cal.Wed,cal.Thur,cal.Fri,cal.Sat,cal.Sun]
    return jsonify( { 'Week Calendar for user '+user_tag:\
                      [{i:Cal[s.index(i)]} for i in s] } )


@app.route('/calendar/api/v1.0/<user_tag>/<task_day>/<time>', methods = ['UDC'])

def UpDateCalendar(user_tag,task_day,time):
    
    calendar1 = ""
    a = None
    for p in Calendar._registry:
        if p.UserTag == user_tag:
            calendar1 = p
            break
    if calendar1 == "":
        abort(404)
    if task_day.lower() == "monday":
        task = calendar1.Mon
    if task_day.lower() == "tuesday":
        task = calendar1.Tues
    if task_day.lower() == "wednesday":
        task = calendar1.Wed
    if task_day.lower() == "thursday":
        task = calendar1.Thur
    if task_day.lower() == "friday":
        task = calendar1.Fri
    if task_day.lower() == "saturday":
        task = calendar1.Sat
    if task_day.lower() == "sunday":
        task = calendar1.Sun
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if time+" o'clock" in request.json and type(request.json[time+" o'clock"])\
                                                                is not unicode:
        abort(400)
    for i in task:
        if i.has_key(time+" o'clock") == True:
           i[time+" o'clock"] = request.json.get(time+" o'clock"\
                                                    ,i[time+" o'clock"])
           a = i
           break
       
    return jsonify( { task_day+" new task for user "+user_tag : a } ) 
   
    
@app.route('/calendar/api/v1.0/<user_tag>', methods = ['GET'])

def get_FullCalendar(user_tag):
    
    calendar1 = ""
    for p in Calendar._registry:
        if p.UserTag == user_tag:
            calendar1 = p
            break
    if calendar1 == "":
        calendar1 = Calendar("default")
        user_tag = "default calendar"
    return jsonify( { 'Week Calendar for '+user_tag: calendar1.FullCal } )
 
@app.route('/calendar/api/v1.0/<user_tag>/<task_day>', methods = ['GET'])

def get_Calendar(user_tag,task_day):
    calendar1 = ""
    for p in Calendar._registry:
        if p.UserTag == user_tag:
            calendar1 = p
            break
    if calendar1 == "":
        abort(400)
    if task_day.lower() == "monday":
        task = calendar1.Mon
    if task_day.lower() == "tuesday":
        task = calendar1.Tues
    if task_day.lower() == "wednesday":
        task = calendar1.Wed
    if task_day.lower() == "thursday":
        task = calendar1.Thur
    if task_day.lower() == "friday":
        task = calendar1.Fri
    if task_day.lower() == "saturday":
        task = calendar1.Sat
    if task_day.lower() == "sunday":
        task = calendar1.Sun
    if len(task) == 0:
        abort(404)
    return jsonify( { task_day+" for user "+user_tag : task } )

@app.route('/calendar/api/v1.0/<user_tag>/<task_day>', methods = ['FFOH'])

def FindFirstOpenHour(user_tag,task_day):
    calendar1 = ""
    day = ""
    Open = True
    a = None
    for p in Calendar._registry:
        if p.UserTag == user_tag:
            calendar1 = p
            break
    if calendar1 == "":
        abort(400)
    if task_day == "any":
        for i in calendar1.FullCal:
            if calendar1.FullCal.index(i) == 0:
                day = 'monday'
            if calendar1.FullCal.index(i) == 1:
                day = 'tuesday'
            if calendar1.FullCal.index(i) == 2:
                day = 'wednesday'
            if calendar1.FullCal.index(i) == 3:
                day = 'thrusday'
            if calendar1.FullCal.index(i) == 4:
                day = 'friday'
            if calendar1.FullCal.index(i) == 5:
                day = 'saturday'
            if calendar1.FullCal.index(i) == 6:
                day = 'sunday'    
            for j in i:
                if j[str(i.index(j)+1)+" o'clock"] == "":
                    Open = False
                    a = j
                    break
    else:
        day = task_day
        if day.lower() == "monday":
            task = calendar1.Mon
        if day.lower() == "tuesday":
            task = calendar1.Tues
        if day.lower() == "wednesday":
            task = calendar1.Wed
        if day.lower() == "thursday":
            task = calendar1.Thur
        if day.lower() == "friday":
            task = calendar1.Fri
        if day.lower() == "saturday":
            task = calendar1.Sat
        if day.lower() == "sunday":
            task = calendar1.Sun
        for i in task:
            if i[str(task.index(i)+1)+" o'clock"] == "":
                Open = False
                a = i
                break
    if Open == False:
        return jsonify( { 'Frist open hour on '+day: a } )
    else:
        abort(404)

@app.route('/calendar/api/v1.0/<user_tag>', methods = ['RESET'])

def Rest_Whole_Calendar(user_tag):
    calendar1 = ""
    for p in Calendar._registry:
        if p.UserTag == user_tag:
            calendar1 = p
            break
    if calendar1 == "":
        abort(400)
    calendar1.erase()
    cal = Calendar(user_tag)
    s = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    Cal = [cal.Mon,cal.Tues,cal.Wed,cal.Thur,cal.Fri,cal.Sat,cal.Sun]
    return jsonify( { 'Week Calendar for user '+user_tag:\
                      [{i:Cal[s.index(i)]} for i in s] } )
 
@app.route('/calendar/api/v1.0/<user_tag>/<task_day>', methods = ['RESET'])

def Rest_Day(user_tag,task_day):
    calendar1 = ""
    for p in Calendar._registry:
        if p.UserTag == user_tag:
            calendar1 = p
            break
    if calendar1 == "":
        abort(400)
    if task_day.lower() == "monday":
        calendar1.resetDay(task_day)
        task = calendar1.Mon
    if task_day.lower() == "tuesday":
        calendar1.resetDay(task_day)
        task = calendar1.Tues
    if task_day.lower() == "wednesday":
        calendar1.resetDay(task_day)
        task = calendar1.Wed
    if task_day.lower() == "thursday":
        calendar1.resetDay(task_day)
        task = calendar1.Thur
    if task_day.lower() == "friday":
        calendar1.resetDay(task_day)
        task = calendar1.Fri
    if task_day.lower() == "saturday":
        calendar1.resetDay(task_day)
        task = calendar1.Sat
    if task_day.lower() == "sunday":
        calendar1.resetDay(task_day)
        task = calendar1.Sun
    return jsonify( { task_day+" for user "+user_tag : task } )

@app.route('/calendar/api/v1.0/<user_tag>/<task_day>/<time>', methods = ['RESET'])

def Rest_Hour(user_tag,task_day,time):
    calendar1 = ""
    for p in Calendar._registry:
        if p.UserTag == user_tag:
            calendar1 = p
            break
    if calendar1 == "":
        abort(400)
    if task_day.lower() == "monday":
        task = calendar1.Mon
    if task_day.lower() == "tuesday":
        task = calendar1.Tues
    if task_day.lower() == "wednesday":
        task = calendar1.Wed
    if task_day.lower() == "thursday":
        task = calendar1.Thur
    if task_day.lower() == "friday":
        task = calendar1.Fri
    if task_day.lower() == "saturday":
        task = calendar1.Sat
    if task_day.lower() == "sunday":
        task = calendar1.Sun
    for i in task:
        if i.has_key(time+" o'clock") == True:
            i[time+" o'clock"] = ""
    return jsonify( { task_day+" for user "+user_tag : task } )

@app.route('/calendar/api/v1.0/<user_tag>', methods = ['DELETE'])

def delete_user(user_tag):
    calendar1 = ""
    for p in Calendar._registry:
        if p.UserTag == user_tag:
            calendar1 = p
            break
    if calendar1 == "":
        abort(400)
    calendar1.erase()
    return jsonify( { 'result': user_tag+" was removed" } )

@app.route('/calendar/api/v1.0/<user_tag>/<task_day>/<time>', methods = ['CDH'])

def CheckDayHour(user_tag,task_day,time):
    calendar1 = ""
    a = None
    for p in Calendar._registry:
        if p.UserTag == user_tag:
            calendar1 = p
            break
    if calendar1 == "":
        abort(400)
    if task_day.lower() == "monday":
        task = calendar1.Mon
    if task_day.lower() == "tuesday":
        task = calendar1.Tues
    if task_day.lower() == "wednesday":
        task = calendar1.Wed
    if task_day.lower() == "thursday":
        task = calendar1.Thur
    if task_day.lower() == "friday":
        task = calendar1.Fri
    if task_day.lower() == "saturday":
        task = calendar1.Sat
    if task_day.lower() == "sunday":
        task = calendar1.Sun
    for i in task:
        if i.has_key(time+" o'clock") == True:
            a = i
            break
    return jsonify( { task_day+" at "+time+" o'clock for user "+user_tag : a } )
    
if __name__ == '__main__':
    app.run(debug = True)
