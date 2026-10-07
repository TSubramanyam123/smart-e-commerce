from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect
)

from sqlalchemy import (
    select,
    desc
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.security import (
    get_current_user
)

from app.models.commerce import (
    Notification
)

from app.services.websocket import (
    manager
)


router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)


@router.get("")
def get_notifications(
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return db.scalars(
        select(Notification)
        .where(
            Notification.user_id ==
            current_user.id
        )
        .order_by(
            desc(
                Notification.created_at
            )
        )
    ).all()


@router.put(
    "/{notification_id}/read"
)
def mark_as_read(
    notification_id: int,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    notification = db.get(
        Notification,
        notification_id
    )

    if (
        not notification
        or notification.user_id !=
        current_user.id
    ):

        return {
            "message":
            "Notification not found"
        }

    notification.is_read = True

    db.commit()

    return {
        "message":
        "Notification marked as read"
    }


@router.put("/read-all")
def mark_all_read(
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    notifications = db.scalars(
        select(Notification).where(
            Notification.user_id ==
            current_user.id,
            Notification.is_read.is_(False)
        )
    ).all()

    for notification in notifications:

        notification.is_read = True

    db.commit()

    return {
        "message":
        "All notifications marked as read"
    }


@router.websocket(
    "/ws/{user_id}"
)
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int
):

    await manager.connect(
        user_id,
        websocket
    )

    try:

        while True:

            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(
            user_id,
            websocket
        )