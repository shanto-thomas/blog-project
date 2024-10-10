#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import uvicorn as uvicorn


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
    if len(sys.argv) > 1 and sys.argv[1] == "runuvicorn":
        # Running the app with uvicorn instead of the default Django runserver
        uvicorn.run("blog_project.asgi:application", host="0.0.0.0", port=8082, reload=True)
    else:
        # Default Django command-line utility
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
