import mongoengine as me
from flask import Flask, redirect, request, jsonify, send_file
from flask_cors import CORS
import secrets

me.connect('redirectutils')
app = Flask(__name__)
CORS(app)

# Initialize Database Structure
class Redirection(me.Document):
    path = me.StringField()
    to = me.StringField()
    password = me.StringField()

@app.route('/')
def IndexPage():
    # Sends a file. This file must contain all css / javascript.
    return send_file('index.html')

@app.route('/<path:link>')
def rd(link):
    to = request.values.get('to')
    password = request.values.get('password')
    delete = request.values.get('delete')
    q = Redirection.objects(path__iexact=link).first()
    if q:
        if delete=='true':
            if password and password==q.password:
                try:
                    q.delete()
                    return jsonify({
                        'code':0,
                        'message':'Operation was done successfully.'
                    })
                except:
                    return jsonify({
                        'code':-2,
                        'message':'Unable to save (database error)'
                    })
            return jsonify({
                'code':-3,
                'message':'Incorrect password'
            })


        if to:
            if not password:
                return jsonify({
                    'code':-1,
                    'message':'This path has been set up to redirect to another website.'
                })
            else:
                if password==q.password:
                    try:
                        q.to=to
                        q.save()
                        return jsonify({
                            'code':0,
                            'message':'Successfully saved.'
                        })
                    except:
                        return jsonify({
                            'code':-2,
                            'message':'Unable to save (Database error)'
                        })
                return jsonify({
                    'code':-3,
                    'message':'Incorrect password.'
                })
        return redirect(q.to)
    else:
        if to:
            try:
                p = secrets.token_urlsafe(16)
                r = Redirection(path=link,to=to,password=p)
                r.save()
                return jsonify({
                    'code':0,
                    'message':'Successfully saved.',
                    'password':p
                })
            except Exception as e:
                print(e)
                return jsonify({
                    'code':-2,
                    'message':'Unable to save. Database error.'
                })

        return '',404
