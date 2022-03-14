from fastapi import Depends
from app.security.auth import JWTCookieAuth, decode_jwt_token
from fastapi.templating import Jinja2Templates
from app.users import User
from postgresql import DBSession

# Configure templates directory
view_templates = Jinja2Templates(directory="templates")


def render_template(request, template, data):
    return view_templates.TemplateResponse(
            template,
            context={
                'request': request,
                **data,
            },
        )


async def get_current_user(jwtoken: str = Depends(JWTCookieAuth())):
    payload = decode_jwt_token(jwtoken)
    with DBSession() as session:
        # This is currently email; change to uuid
        user = User.get_by_email(db_session=session, email=payload['user_email'])
        return user



