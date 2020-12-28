FROM python
MAINTAINER Kaspars Mickevics (kaspars@fx.lv)
RUN git clone https://github.com/fxlv/python_testing.git
WORKDIR /python_testing/smarthome
RUN pip install -r requirements.txt
ENTRYPOINT ["python","colorize.py"]
