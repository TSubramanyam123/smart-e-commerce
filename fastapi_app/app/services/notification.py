from sqlalchemy.orm import Session

from app.models.commerce import Notification

from app.services.websocket import manager

from app.services.email import send_email


async def create_notification(
    db: Session,
    user_id: int,
    notification_type: str,
    message: str,
    email: str | None = None
):

    notification = Notification(
        user_id=user_id,
        type=notification_type,
        message=message,
        is_read=False
    )

    db.add(notification)

    db.commit()

    db.refresh(notification)

    await manager.send(
        user_id,
        {
            "type": notification_type,
            "message": message,
            "notification_id":
                notification.id
        }
    )

    if email:

        send_email(
            email,
            f"Order Update - {notification_type}",
            message
        )

    return notification