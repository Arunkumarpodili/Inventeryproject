FROM almalinux

COPY requirements.txt .

RUN yum install python -y 

RUN pip3 install --no-cache-dir -r requirements.txt

RUN yum install nginx -y

RUN rm -rf /usr/share/nginx/html/index.html

COPY INVENTERY_APPLICATION /usr/share/nginx/html/

EXPOSE 85:80

CMD ["nginx", "-g", "daemon off;"]


