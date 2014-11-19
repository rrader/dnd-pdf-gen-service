FROM    centos:6.4

# Enable EPEL
RUN     rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm

# SSH
EXPOSE 22
RUN yum -y groupinstall "Development tools"
RUN yum -y install rsyslog openssh-server screen passwd java-1.6.0-openjdk sudo
RUN sed 's/UsePAM yes/UsePAM no/' -i /etc/ssh/sshd_config
RUN sed 's/#PermitRootLogin yes/PermitRootLogin yes/' -i /etc/ssh/sshd_config
RUN sed 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/' -i /etc/ssh/sshd_config

RUN /etc/init.d/sshd restart


RUN adduser -d {{ home }} {{ juser }}
RUN echo 'root:{{ root_password }}' | chpasswd
RUN echo '{{ juser }}:{{ password }}' | chpasswd
RUN su - {{ juser }} -c "mkdir {{ home }}/.ssh"
ADD id_rsa {{ home }}/.ssh/
ADD id_rsa.pub {{ home }}/.ssh/
ADD known_hosts {{ home }}/.ssh/
ADD authorized_keys {{ home }}/.ssh/
RUN chown {{ juser }}:{{ juser }} -R {{ home }}/.ssh
RUN chmod 0700 {{ home }}/.ssh && chmod 0600 {{ home }}/.ssh/*


RUN sed 's/Defaults *requiretty/#Defaults    requiretty/' -i /etc/sudoers
RUN echo "{{ juser }} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN su - {{ juser }} -c "wget -O {{ home }}/swarm-client-1.9-jar-with-dependencies.jar http://maven.jenkins-ci.org/content/repositories/releases/org/jenkins-ci/plugins/swarm-client/1.9/swarm-client-1.9-jar-with-dependencies.jar"

ENTRYPOINT ["/usr/sbin/sshd"]
CMD ["-D"]
