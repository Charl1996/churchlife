from app.routers.decorators import view_request
from fastapi import Request, Depends
from app.organisations import Organisation
from app.users import User
from app.routers.helper import get_current_user
from postgresql import DBSession
from fastapi import APIRouter

router = APIRouter()


@router.get('/{domain}/dashboard')
@view_request
def dashboard(request: Request, domain: str, user: User = Depends(get_current_user)):
    with DBSession() as db_session:
        org = Organisation.get_by_domain(db_session=db_session, domain=domain)
        # And some other stuff...
    return {
        'template': "/layout_content/dashboard.html",
        'data': {
            'organisation': {
                'name': org.fields.name,
            },
        }
    }
