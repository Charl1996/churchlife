from app.routers.decorators import view_request, domain_request
from fastapi import Request, Depends
from app.organisations import Organisation
from app.users import User
from app.routers.helper import get_current_user
from postgresql import DBSession
from fastapi import APIRouter

router = APIRouter()


@router.get('/{domain}/dashboard')
@view_request
@domain_request
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


@router.get('/{domain}/settings')
@view_request
@domain_request
def settings(request: Request, domain: str, user: User = Depends(get_current_user)):
    with DBSession() as db_session:
        org = Organisation.get_by_domain(db_session=db_session, domain=domain)

    return {
        'template': '/layout_content/settings.html',
        'data': {
            'organisation': {
                'name': org.fields.name,
                # 'logo': org.fields.logo,
            }
        }
    }


@router.get('/{domain}/users')
@view_request
@domain_request
def users(request: Request, domain: str, user: User = Depends(get_current_user)):
    with DBSession() as db_session:
        org = Organisation.get_by_domain(db_session=db_session, domain=domain)

    return {
        'template': '/layout_content/users.html',
        'data': {
            'organisation': {
                'name': org.fields.name,
                # 'logo': org.fields.logo,
            }
        }
    }


@router.get('/{domain}/database')
@view_request
@domain_request
def database(request: Request, domain: str, user: User = Depends(get_current_user)):
    with DBSession() as db_session:
        org = Organisation.get_by_domain(db_session=db_session, domain=domain)

    return {
        'template': '/layout_content/database.html',
        'data': {
            'organisation': {
                'name': org.fields.name,
                # 'logo': org.fields.logo,
            }
        }
    }


@router.get('/{domain}/messaging')
@view_request
@domain_request
def messaging(request: Request, domain: str, user: User = Depends(get_current_user)):
    with DBSession() as db_session:
        org = Organisation.get_by_domain(db_session=db_session, domain=domain)

    return {
        'template': '/layout_content/messaging.html',
        'data': {
            'organisation': {
                'name': org.fields.name,
                # 'logo': org.fields.logo,
            }
        }
    }
