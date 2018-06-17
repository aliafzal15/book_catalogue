import os

from bookcat import app
from shared_models import db
from bookcat.auth.models import User
db.create_all()

if not User.query.filter_by(user_name='testuser').first():
     User.create_user(user ='testuser',
                      email ='ali@myseat.com',
                      password ='secret'
                    )


port = int(os.environ.get('PORT', 5004))
app.run(debug=True, host='0.0.0.0', port=port)




