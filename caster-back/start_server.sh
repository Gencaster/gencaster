#!/bin/sh

sleep 2;

echo "Apply database migrations";
python manage.py migrate;

echo "Check if SuperUser exists";
if [ -z "$DJANGO_SU_USER" ];
then
    echo "No Superuser given";
else
    python_script="from django.contrib.auth import get_user_model; User = get_user_model();  User.objects.create_superuser('"$DJANGO_SU_USER"', '', '"$DJANGO_SU_PASS"') if not User.objects.filter(username='"$DJANGO_SU_USER"').exists() else print('Superuser exists already')";
    python manage.py shell --command "$python_script";
fi;

echo "Collect static files"

python manage.py collectstatic --noinput > /dev/null

if ! [ -z "$DEVELOPMENT" ]; then
    echo "Start development server";
    uvicorn gencaster.asgi:application --reload --host 0.0.0.0 --port 8000
        # --header "Access-Control-Allow-Origin:*" \
        # --header "Access-Control-Allow-Methods:OPTIONS, GET, POST" \
        # --header "Access-Control-Allow-Headers:Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, If-Modified-Since, X-File-Name, Cache-Control" \
        # --header "Access-Control-Allow-Credentials:true"
else
    echo "Starting gunicorn server";
    gunicorn \
        gencaster.asgi:application \
        -k uvicorn.workers.UvicornWorker \
        -c gencaster/gunicorn.conf.py \
        --reload \
        # --header "Access-Control-Allow-Origin:dev.gencaster.org,editor.dev.gencaster.org" \
        # --header "Access-Control-Allow-Methods:OPTIONS, GET, POST" \
        # --header "Access-Control-Allow-Headers:Content-Type, Depth, User-Agent, X-File-Size, X-Requested-With, If-Modified-Since, X-File-Name, Cache-Control" \
        # --header "Access-Control-Allow-Credentials:true"
        --capture-output;
fi
