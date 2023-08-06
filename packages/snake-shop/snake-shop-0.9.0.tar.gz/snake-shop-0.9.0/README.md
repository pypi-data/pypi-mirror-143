Reset Order and Basket id to 1
./manage.py shell_plus
Order.objects.all().delete()
Basket.objects.all().delete()

./manage.py dbshell
BEGIN;
SELECT setval(pg_get_serial_sequence('"order_order"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "order_order";
SELECT setval(pg_get_serial_sequence('"basket_basket"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "basket_basket";
COMMIT;

# Alternativ SQL:
ALTER SEQUENCE order_order_id_seq RESTART WITH 1;
ALTER SEQUENCE basket_basket_id_seq RESTART WITH 1;
SELECT setval('order_order_id_seq', 1, FALSE);
SELECT setval('basket_basket_id_seq', 1, FALSE);





Sync Shop data:
curlftpfs ftp.5768678463571.hostingkunde.de /mnt/old_server
rsync -ah /mnt/old_server /root/old_server


Dump DB (eg. on Prod):
./manage.py dumpdata --indent 2 -o db_dump_X.json


Restore DB (eg. on Dev):
python manage.py flush #--noinput
python3 manage.py shell -c "from django.contrib.contenttypes.models import ContentType;ContentType.objects.all().delete();quit()"
python manage.py loaddata db_dump.json -e contenttypes -e auth.Permission -e admin
