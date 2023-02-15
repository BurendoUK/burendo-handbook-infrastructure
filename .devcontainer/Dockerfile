# Start from the latest Ubuntu LTS image
FROM ubuntu:focal

# Set the shell to zsh
SHELL ["/bin/zsh", "-c"]

# Install zsh, git, and other dependencies
RUN apt-get update \
  && apt-get install -y zsh git python3 python3-pip unzip curl \
  && sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
  && chsh -s $(which zsh) root

# Install AWS CLI and awsume
RUN pip3 install awscli awsume

# Install Terraform
RUN curl -O https://releases.hashicorp.com/terraform/1.2.6/terraform_1.2.6_linux_amd64.zip \
  && unzip terraform_1.2.6_linux_amd64.zip \
  && mv terraform /usr/local/bin/ \
  && rm terraform_1.2.6_linux_amd64.zip

# Set the default shell to zsh
ENTRYPOINT ["/bin/zsh"]
