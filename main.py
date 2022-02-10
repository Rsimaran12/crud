import os
from tabnanny import filename_only
from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import flash, jsonify, redirect, render_template, request, url_for
import gridfs

@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        name = request.form.get("name")
        image = request.files["image"]
        summary = request.form.get("summary")
        if name and image and summary and image.filename.split(".")[-1].lower():
            filename = filename_only(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            mongo.db.gallery.insert_one({
                "filename": filename,
                "name": name.strip(),
                "summary": summary.strip()
            })

            flash("Successfully uploaded image to gallery!", "success")
            return redirect(url_for("upload"))
        else:
            flash("An error occurred while uploading the image!", "danger")
            return redirect(url_for("upload"))
    return render_template("upload.html")
		
@app.route('/users')
def users():
	users = mongo.db.user.find()
	resp = dumps(users)
	return resp
		
@app.route('/user/<id>')
def user(id):
	user = mongo.db.user.find_one({'_id': ObjectId(id)})
	resp = dumps(user)
	return resp

@app.route('/update', methods=['PUT'])
def update_user():
	_json = request.json
	_id = _json['_id']
	_name = _json['name']
	_img = _json['img']
	_summary = _json['summary']		
	# validate the received values
	if _name and _img and _summary and _id and request.method == 'PUT':
        #do not save password as a plain text
		# _hashed_password = generate_password_hash(_password)
		# save edits
		mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$id' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'img': _img, 'summary':_summary}})
		resp = jsonify('Data updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
	mongo.db.user.delete_one({'_id': ObjectId(id)})
	resp = jsonify('Data deleted successfully!')
	resp.status_code = 200
	return resp
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
         }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

# if __name__ == "__main__":
#     app.run()