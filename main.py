from fastapi import FastAPI, APIRouter, status
from models import User
from schemas import UserModel
from database import Session, engine
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

session = Session(bind=engine)

app = FastAPI()


@app.get("/")
async def welcome():
    return {"Message": "welcome"}


@app.post("/user", status_code=status.HTTP_201_CREATED)
async def add_user(user: UserModel):
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the email already exists"
                             )

    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the email already exists"
                             )

    new_user = User(
        username=user.username,
        email=user.email,
        gender=user.gender,
        roles=user.roles
    )

    session.add(new_user)
    session.commit()
    return new_user


@app.get('/user/{username}/')
async def get_specific_user(username: str):
    current_user = session.query(User).filter(User.username == username).first()
    if current_user:
        return jsonable_encoder(current_user)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No user with this name"
                        )


# update user details
@app.put('/user/update/{username}/')
async def update_order(username: str, user: UserModel):
    user_to_update = session.query(User).filter(User.username == username).first()
    if user_to_update:
        user_to_update.roles = user.roles
        user_to_update.email = user.email
        user_to_update.gender = user.gender

        session.commit()

        response = {
            "username": user_to_update.username,
            "email": user_to_update.email,
            "roles": user_to_update.roles,
        }

        return jsonable_encoder(user_to_update)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No user with this name"
                        )


# delete an user
@app.delete('/user/delete/{username}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_user(user: str, username: str):
    """
        ## Delete an Order
        This deletes an order by its ID
    """

    user_to_delete = session.query(User).filter(User.username == user).first()
    user_role = session.query(User).filter(User.username == username).first()

    if user_role.roles == 'ADMIN':
        if user_to_delete:
            session.delete(user_to_delete)

            session.commit()

            return user_to_delete
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No user with this name"
                            )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User not permitted to delete"
                            )


# get the user if my current user role == ADMIN

@app.get('/user/admin/{username}/')
async def get_specific_user(username: str, skip: int = 0, limit: int = 100):
    user_role = session.query(User).filter(User.username == username).first()

    if user_role.roles == 'ADMIN':
        return session.query(User).offset(skip).limit(limit).all()
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="NOT_PERMITTED_ACTION!"
                        )
