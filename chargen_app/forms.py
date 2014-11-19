from django import forms

class DockerfileRequestForm(forms.Form):
    OSs = (
        ('centos6', 'CentOS 6'),
        ('centos5', 'CentOS 5'),
        ('opensuse12', 'OpenSUSE 12'),
        ('debian6', 'Debian 6 Squeeze'),
        )
    os = forms.ChoiceField(label='OS', choices=OSs, initial='centos6')
    # ssh = forms.BooleanField(label='SSH enabled', initial=True)
    juser = forms.CharField(label='Username', initial='jenkins')
    home = forms.CharField(label='Home directory', initial='/var/lib/jenkins')
    password = forms.CharField(label='Password', initial='1111')
    root_password = forms.CharField(label='Root password', initial='1111')

    JenkinsConnections = (
        ('swarm', 'Swarm plugin'),
        )
    jenkins_connection = forms.ChoiceField(label='Jenkins connection', choices=JenkinsConnections, initial='centos6')
