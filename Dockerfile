FROM nvidia/cudagl:10.0-devel-ubuntu18.04

# base packages
RUN echo "deb http://ppa.launchpad.net/apt-fast/stable/ubuntu bionic main" >> /etc/apt/sources.list || exit 1; \
    echo "deb-src http://ppa.launchpad.net/apt-fast/stable/ubuntu bionic main" >> /etc/apt/sources.list || exit 1; \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A2166B8DE8BDC3367D1901C11EE2FF37CA8DA16B || exit 1; \
    apt-get update || exit 1; \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y --no-install-recommends -o Dpkg::Options::="--force-confnew" || exit 1; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends -o Dpkg::Options::="--force-confnew" \
    apt-utils apt-fast || exit 1; \
    echo debconf apt-fast/maxdownloads string 5 | debconf-set-selections || exit 1; \
    echo debconf apt-fast/dlflag boolean true | debconf-set-selections || exit 1; \
    echo debconf apt-fast/aptmanager string apt-get | debconf-set-selections || exit 1
RUN DEBIAN_FRONTEND=noninteractive apt-fast install -y --no-install-recommends -o Dpkg::Options::="--force-confnew" \
    dh-make fakeroot build-essential pkg-config devscripts lsb-release gdb bash-completion command-not-found || exit 1
RUN DEBIAN_FRONTEND=noninteractive apt-fast install -y --no-install-recommends -o Dpkg::Options::="--force-confnew" \
    sudo psmisc openssh-client nmap netcat-openbsd rsync axel git vim screen unrar unzip ccache less locales || exit 1
RUN DEBIAN_FRONTEND=noninteractive apt-fast install -y --no-install-recommends -o Dpkg::Options::="--force-confnew" \
    python3-dev python3-pip python3-setuptools python3-argcomplete || exit 1

# bash + python3 tab completion and locale setup
RUN echo '\n\
if [ -f /usr/share/bash-completion/bash_completion ]; then\n\
  . /usr/share/bash-completion/bash_completion\n\
elif [ -f /etc/bash_completion ]; then\n\
  . /etc/bash_completion\n\
fi\n' >> /etc/bash.bashrc || exit 1; \
    activate-global-python-argcomplete3 || exit 1; \
    locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8

# fix for cv2/Qt and matplotlib/tkinter stuff
RUN DEBIAN_FRONTEND=noninteractive apt-fast install -y --no-install-recommends -o Dpkg::Options::="--force-confnew" \
    libsm6 libice6 python3-tk || exit 1

# copy and extract cudnn
ADD cudnn/libcudnn7_7.6.0.64-1+cuda10.0_amd64.deb /tmp/cudnn.deb
RUN dpkg -i /tmp/cudnn.deb || exit 1

# copy datasets
ADD datasets/acfr-fruit-dataset.zip /tmp/acfr-fruit-dataset.zip
ADD datasets/plant-pathology-2020-fgvc7.zip /tmp/plant-pathology-2020-fgvc7.zip

# setup demo user and home permissions
ARG myuser
ARG mygroup
RUN mygid=$(awk -F\: '/users/ {print $3}' /etc/group); \
    adduser --gecos "" --disabled-password --gid ${mygid} ${myuser} || exit 1; \
    echo "${myuser} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers || exit 1; \
    chown -LR ${myuser}:${mygroup} /home/${myuser} || exit 1

# copy all the stuff
ARG mytarget=/tmp/orchard
ADD weights ${mytarget}/weights
ADD Mask_RCNN ${mytarget}/Mask_RCNN
ADD scripts ${mytarget}/scripts
ADD orchard ${mytarget}/orchard
ADD samples ${mytarget}/samples
ADD setup.py ${mytarget}/setup.py

# extract datasets, install dependencies and install the orchard package
RUN chown -R ${myuser}:${mygroup} ${mytarget} || exit 1
RUN sudo -H -u ${myuser} ${mytarget}/scripts/install_datasets.sh || exit 1
RUN sudo -H -u ${myuser} ${mytarget}/scripts/install.sh || exit 1

# apt-get and /tmp clean-up
RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* /tmp/*
