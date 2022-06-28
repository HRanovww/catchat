import os
import sys

import click
from flask import Flask

from catchat.settings import config
from catchat.extension import db
from catchat.blueprints.auth import auth_bp
from catchat.blueprints.chat import chat_bp
from catchat.models import User


WIN = sys.platform.startswith('win')


def create_app(config_name=None):
    app = Flask(__name__)

    load_config(app, config_name)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    register_blueprint(app)

    register_commands(app)

    return app


def load_config(app, config_name):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    prefix = 'sqlite:///' if WIN else 'sqlite:////'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_URL',
            prefix + os.path.join(app.instance_path, 'data.db'))

    app.config.from_object(config[config_name])


def register_blueprint(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--message', default=300, help='Quantity of messages, default is 300.')
    def forge(message):
        """Generate fake data."""
        # import random
        from sqlalchemy.exc import IntegrityError

        from faker import Faker

        fake = Faker()

        click.echo('Initializing the database...')
        db.drop_all()
        db.create_all()

        click.echo('Forging the data...')
        admin = User(nickname='Haoran', email='m646848374@qq.com')
        admin.set_password('302112')
        db.session.add(admin)
        db.session.commit()

        click.echo('Generating user...')
        for i in range(50):
            user = User(nickname=fake.name(),
                        bio=fake.sentence(),
                        github=fake.url(),
                        website=fake.url(),
                        email=fake.email()
                        )
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        click.echo('Generating messages...')
        for i in range(message):
            pass
        click.echo('Done.')
