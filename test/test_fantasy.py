import main
from nose import with_setup
import tempfile
from nose.tools import eq_

class TestFantasyFlask:
    
    def setup(self):
        tmpfile=tempfile.mkstemp()
        main.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+tmpfile[1]
        self.app=main.app.test_client()
        main.db.create_all()
        
        
    def test_register(self):
        self.app.post('/register', data=dict(email='eric', password='ngeo'))
        qry=main.User.query.filter_by(username='eric').first()
        eq_(qry.username,'eric')
        eq_(qry.password,'ngeo')
        self.app.post('/register', data=dict(email='bbbb', password='dddd'))
        qry=main.User.query.filter_by(username='bbbb').first()
        eq_(qry.username, 'bbbb')
        eq_(qry.password, 'dddd')

    def test_login(self):
        self.app.get('handle_login', data=dict(oauth_verifier='hello'))
        