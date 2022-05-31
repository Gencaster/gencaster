from django.apps import AppConfig


class StreamConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stream"

    def ready(self) -> None:
        from .models import Stream

        try:
            Stream.objects.disconnect_all_streams()
        except Exception as e:
            print(f"Could not reset all streams: {e}")
        return super().ready()
