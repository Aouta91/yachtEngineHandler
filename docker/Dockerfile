FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y && apt-get install -y software-properties-common locales \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen \
    && rm -rf /var/lib/apt/lists/* \
    && add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main" \
    && apt-get update && apt-get install -y \
        build-essential \
        python3 \
        python3-pip \
        python3-dev \
        libsm6 \
    	libxext6 \
    	libfontconfig1 \
    	libxrender1 \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libjasper-dev \
        libavformat-dev \
        libpq-dev \
    	libturbojpeg \
    	libgl1-mesa-glx \
	&& python3 -m pip install --upgrade pip \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

CMD mkdir -p /workspace

COPY . /workspace/
RUN python3 -m pip install -r /workspace/requirements.txt

WORKDIR /workspace

EXPOSE 8000

ENTRYPOINT ["bash", "-c", "uvicorn server:app --reload --host=0.0.0.0"]
