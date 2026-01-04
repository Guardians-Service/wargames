FROM kalilinux/kali-rolling

# 기본 도구 + ttyd 빌드 도구 설치
RUN apt-get update && apt-get install -y \
    git cmake g++ libjson-c-dev libwebsockets-dev make curl bash \
    nmap netcat-openbsd wget dnsutils whois \
    net-tools iputils-ping iproute2 \
    hydra john \
    sqlmap nikto whatweb \
    python3 python3-pip python3-venv \
    gdb radare2 binwalk \
    tcpdump


# ttyd 소스 클론 및 빌드
RUN git clone https://github.com/tsl0922/ttyd.git && \
    cd ttyd && mkdir build && cd build && \
    cmake -DDEFAULT_PORT=8000 .. && make && make install && \
    cd / && rm -rf /ttyd

# 포트 노출 및 실행
EXPOSE 8000
CMD ["ttyd", "--writable", "-p", "8000", "bash"]