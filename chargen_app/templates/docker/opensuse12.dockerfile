FROM    flavio/opensuse-12-3

RUN zypper addrepo --no-gpgcheck http://download.opensuse.org/repositories/Java:/openjdk6:/Factory/SLE_11_SP2/Java:openjdk6:Factory.repo
RUN zypper addrepo --no-gpgcheck http://download.tizen.org/tools/latest-release/openSUSE_12.1/ tools

RUN zypper refresh
RUN zypper install -y git openssh sudo wget
RUN zypper install -y java-1_6_0-openjdk-devel

RUN sed 's/UsePAM yes/UsePAM no/' -i /etc/ssh/sshd_config
RUN sed 's/#PermitRootLogin yes/PermitRootLogin yes/' -i /etc/ssh/sshd_config
RUN sed 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/' -i /etc/ssh/sshd_config

RUN /etc/init.d/sshd restart

RUN useradd -md {{ home }} {{ juser }}
RUN echo 'root:{{ root_password }}' | chpasswd
RUN echo '{{ juser }}:{{ password }}' | chpasswd
RUN su - {{ juser }} -c "mkdir {{ home }}/.ssh"
ADD id_rsa {{ home }}/.ssh/
ADD id_rsa.pub {{ home }}/.ssh/
ADD known_hosts {{ home }}/.ssh/
ADD authorized_keys {{ home }}/.ssh/
RUN chown {{ juser }}:users -R {{ home }}/.ssh
RUN chmod 0700 {{ home }}/.ssh && chmod 0600 {{ home }}/.ssh/*

RUN sed 's/Defaults *requiretty/#Defaults    requiretty/' -i /etc/sudoers
RUN echo "{{ juser }} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN su - {{ juser }} -c "wget -O {{ home }}/swarm-client-1.9-jar-with-dependencies.jar http://maven.jenkins-ci.org/content/repositories/releases/org/jenkins-ci/plugins/swarm-client/1.9/swarm-client-1.9-jar-with-dependencies.jar"

ENTRYPOINT ["/usr/sbin/sshd"]
CMD ["-D"]
