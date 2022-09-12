from flask.cli import FlaskGroup
from src import create_app, db
from src.config import config_dict


app = create_app(config=config_dict['test'])

cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()