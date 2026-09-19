from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

def import_all_models() -> None:
    from app.modules.auth import models as _auth_models
    from app.modules.route import models as _route_models
    from app.modules.run_tracking import models as _run_models
    from app.modules.territory import models as _territory_models
