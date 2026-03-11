from celery import Celery


def celery_init_app(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY"])

    class FlaskTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = FlaskTask
    return celery
