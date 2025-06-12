@app.route('/some_route')
def some_function():
    return redirect(url_for('verify_page'))
