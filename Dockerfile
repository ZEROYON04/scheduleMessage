FROM python
RUN sudo apt update && \
sudo apt install xvfb && \
pip3 install playwright && \
pip install APScheduler && \
playwright install
WORKDIR /sendMessageApp
COPY ./lineMessage /sendMessageApp/
CMD ["xvfb-run", "-a", "python3", "sendMessage.py"]