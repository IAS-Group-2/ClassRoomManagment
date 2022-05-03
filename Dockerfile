FROM python:3.6
RUN mkdir /project
RUN apt-get update && \ 
    apt-get install -y python3 && \ 
    apt install -y python3-pip && \ 
    DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC && \ 
    apt-get install -y tzdata && \ 
    apt-get install -y ffmpeg libsm6 libxext6 && \ 
    cd /project
WORKDIR /project/ 
COPY ./requirements.txt /project/requirements.txt
RUN pip install cmake
RUN pip install -r requirements.txt 
COPY . /project/
EXPOSE 5000
ENTRYPOINT ["python3" , "app.py"] 
