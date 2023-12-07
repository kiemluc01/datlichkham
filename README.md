# Website đặt lịch phòng khám
## khởi tạo môi trường
pip install virtualenv
python3.10 -m virtualenv .env

## activate môi trường
source .env/bin/activate   macos, linux
.env/Scripts/activate  windonws

## cài các thư viện cần thiết
pip install -r requirements.txt

## runserver
python manage.py runserver