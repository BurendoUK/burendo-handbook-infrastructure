FROM mcr.microsoft.com/devcontainers/base:jammy

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
  software-properties-common \
  curl \
  git \
  zsh \
  sudo \
  unzip \
  && add-apt-repository ppa:deadsnakes/ppa \
  && apt-get update \
  && apt-get install -y python3.8 \
  python3-pip \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install nodejs
RUN curl -fsSL https://deb.nodesource.com/setup_19.x | sudo -E bash - && \
  sudo apt-get install -y nodejs build-essential gcc g++ make

# Install AWS CLI and awsume
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
  unzip awscliv2.zip && \
  ./aws/install && \
  pip3 install awsume \
  boto3 \
  Jinja2 \
  PyYAML

# Configure ZSH
ENV USER=vscode
RUN usermod -s /bin/zsh ${USER} && \
  rm -rf /root/.oh-my-zsh && \
  sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended && \
  echo "alias awsume='. awsume'" >> /home/${USER}/.oh-my-zsh/custom/aliases.zsh

# Mount the .aws folder
ARG AWS_HOME=/home/${USER}/.aws
RUN mkdir -p ${AWS_HOME}
VOLUME ["${AWS_HOME}"]

# Install ZSH plugins
RUN git clone https://github.com/zsh-users/zsh-autosuggestions /home/${USER}/.oh-my-zsh/custom/plugins/zsh-autosuggestions && \
  git clone https://github.com/zsh-users/zsh-syntax-highlighting.git /home/${USER}/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting

# Install Terraform version manager (tfenv) and Terraform 1.2.6
RUN git clone https://github.com/tfutils/tfenv.git /usr/local/tfenv && \
  ln -s /usr/local/tfenv/bin/* /usr/local/bin/ && \
  tfenv install 1.2.6 && \
  tfenv use 1.2.6

# Set the default shell to ZSH and source .zshrc
SHELL ["/bin/zsh", "-l"]
CMD ["zsh", "-lc", "source ~/.zshrc; zsh"]

USER vscode
WORKDIR /home/vscode
