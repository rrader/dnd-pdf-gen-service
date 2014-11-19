FROM cduez/squeeze:squeeze

# SSH
EXPOSE 22
RUN apt-get update
RUN apt-get -y install openssh-server sudo wget
RUN mkdir -p /var/run/sshd
RUN sed 's/UsePAM yes/UsePAM no/' -i /etc/ssh/sshd_config
RUN sed 's/#PermitRootLogin yes/PermitRootLogin yes/' -i /etc/ssh/sshd_config
RUN sed 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/' -i /etc/ssh/sshd_config
RUN /usr/sbin/sshd


RUN apt-get -y install build-essential

RUN useradd -m -d {{ home }} {{ juser }}
RUN echo 'root:{{ root_password }}' | chpasswd
RUN echo '{{ juser }}:{{ password }}' | chpasswd
RUN su - {{ juser }} -c "mkdir -p {{ home }}/.ssh"
ADD id_rsa {{ home }}/.ssh/
ADD id_rsa.pub {{ home }}/.ssh/
ADD known_hosts {{ home }}/.ssh/
ADD authorized_keys {{ home }}/.ssh/
RUN chown {{ juser }}:{{ juser }} -R {{ home }}/.ssh
RUN chmod 0700 {{ home }}/.ssh && chmod 0600 {{ home }}/.ssh/*


RUN sed 's/Defaults *requiretty/#Defaults    requiretty/' -i /etc/sudoers
RUN echo "{{ juser }} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN apt-get -y install openjdk-6-jre-headless git

RUN su - {{ juser }} -c "wget -O {{ home }}/swarm-client-1.9-jar-with-dependencies.jar http://maven.jenkins-ci.org/content/repositories/releases/org/jenkins-ci/plugins/swarm-client/1.9/swarm-client-1.9-jar-with-dependencies.jar"

ENTRYPOINT ["/usr/sbin/sshd"]
CMD ["-D"]
