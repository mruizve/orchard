#!/usr/bin/env bash

whereami=$(grep nvidia-docker /proc/1/cgroup)
if [ ! -z "$whereami" ]; then
  # script not loaded inside containers
  return
fi

export myimage="mruizve/orchard:latest"
export myhost="orchard-demo-container"
export myuser="demo"
export mygroup="users"
export mysteupdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)/.."
export myjupyterport=8888

function orchard_build() {
  pushd ${mysteupdir} >/dev/null

  nvidia-docker build --rm -t "${myimage%:*}" \
    --build-arg myuser="${myuser}" \
    --build-arg mygroup="${mygroup}" \
    -f Dockerfile .
  code=$?

  popd >/dev/null 2>&1

  return ${code}
}

function orchard_stop() {
  nvidia-docker stop "${myhost}"
  nvidia-docker rm "${myhost}"
}

function orchard_start() {
  # grab the container status
  container=$(nvidia-docker inspect -f '{{.State.Pid}}' ${myhost} 2>/dev/null)
  code=$?
  run=0

  # does the container need to be created?
  if [ "${code}" -ne "0" ]; then
    # create it based on the latest image available
    run=1
  else
    # verify its image version
    image=$(nvidia-docker inspect -f "{{.Id}}" ${myimage%:*} 2>/dev/null)
    current=$(nvidia-docker inspect -f "{{.Image}}" ${myhost})
    if [ "${image}" != "${current}" ]; then
      echo "a new image version has been released."
      echo "do you wish to update the container image?"
      echo "WARNING: all running processes will be killed"
      select answer in "Yes" "No"; do
        case $answer in
          Yes )
            # update it based on the latest image available
            orchard_stop
            run=1
            break;;
          No )
            break;;
        esac
      done
    fi
  fi

  # need to create the container?
  if [ "$run" -eq "1" ]; then
    # verify image existence
    image=$(nvidia-docker inspect -f "{{.Id}}" ${myimage%:*} 2>/dev/null)
    code=$?
    if [ "${code}" -ne "0" ]; then
      # create image
      orchard_build || return
    fi

    nvidia-docker run -d -it \
      -v "/tmp/.X11-unix:/tmp/.X11-unix:rw" \
      -p ${myjupyterport}:${myjupyterport} \
      --env "USER=${myuser}" --env="DISPLAY" \
      --user="${myuser}:${mygroup}" -h "${myhost}" \
      --name "${myhost}" \
      ${myimage} bin/bash

    # get container pid
    container=$(nvidia-docker inspect -f '{{.State.Pid}}' "${myhost}" 2>/dev/null)
  fi

  # does the container have been stopped?
  if [ "$container" -eq "0" ]; then
    nvidia-docker start "${myhost}"
  fi
}

function orchard_exec () {
  # validate input arguments
  if [ "$#" -eq 0 ]; then
    echo "usage: orchard_exec cmd"
  else
    # initialize or update the container (if required/desired)
    orchard_start

    # spawn a new process inside the container
    nvidia-docker exec --user="${myuser}:${mygroup}" --workdir "/home/${myuser}" -it "${myhost}" "$@"
  fi
}

function orchard_enter() {
  orchard_exec bash
}

function orchard_jupyter() {
  orchard_exec jupyter notebook --ip=0.0.0.0 --port=${myjupyterport} --allow-root
}

function orchard_reborn() {
  orchard_stop
  orchard_enter
}

# allow to execute graphical applications inside containers
if [ -n "$SSH_CLIENT" ]; then  # ssh connection ...
  if [ -z "$DISPLAY" ]; then   # ... without X forwarding
    export DISPLAY=$(who|awk '$2 ~ /tty/ { print $5 }'|tr -d '()')
  fi
fi

# allow container to connect the X server
xhost +local:root >/dev/null

# export functions only outside container
export -f orchard_stop
export -f orchard_start
export -f orchard_exec
export -f orchard_enter
export -f orchard_jupyter
export -f orchard_reborn
