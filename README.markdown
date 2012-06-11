# A Recipe for a mod_passenger RPM on CentOS built against Ruby Enterprise Edition

Perform the following on a build box as root.

## Create an RPM Build Environment

You can accomplish this task in two different ways: The Vagrant way and The Regular way

### Create an RPM Build Environment: The Vagrant way

If you're familiar with Vagrant (http://vagrantup.com), just do the following:

    # Download the vagrant box on https://docs.google.com/uc?id=0B8SJKPjjPVibWlkwZG1wckVQTlU&export=download
    vagrant box add centos58-builder <path-to-the-downloaded-box>
    vagrant init centos58-builder
    vagrant up
    vagrant ssh

The box used in Vagrant is already prepared for RPM Creation. However, you can still prepare the box
by your own, just following the next section in this document.

### Create an RPM Build Environment: The Regular way

You'll need to perform these tasks:

#### Prepare the RPM Build Environment

    yum install rpmdevtools
    rpmdev-setuptree

#### Install Ruby Enterprise Edition and its rubygems as dependencies

    git clone git://github.com/rafaelfelix/passenger-ree-centos.git
    cd passenger-ree-centos/deps
    rpm -ivh ruby-enterprise*
    
WARNING: These RPMs were built on an Centos 5.8 machine (EL5). If you want to build your own RPMs, please refer to:

    https://github.com/rafaelfelix/ree-centos

#### Install Prerequisites for RPM Creation

    yum groupinstall 'Development Tools'
    yum install zlib-devel httpd-devel curl-devel

## Download Passenger

    cd /tmp
    gem fetch passenger --version 3.0.12
    tar xvf passenger-3.0.12.gem
    mv data.tar.gz ~/rpmbuild/SOURCES/passenger-3.0.12.tar.gz

## Get Necessary System-specific Configs

    cp passenger-ree-centos/spec/mod_passenger-ree.spec ~/rpmbuild/SPECS/

## Build the RPM

    cd ~/rpmbuild/
    # the QA_RPATHS var tells the builder to ignore file path errors
    QA_RPATHS=$[ 0x0002 ] rpmbuild -ba SPECS/mod_passenger-ree.spec

The resulting RPM will be:

    ~/rpmbuild/RPMS/x86_64/mod_passenger-ree-3.0.12-1.x86_64.rpm

Remember to build the RPM using an unprivileged user! More information on http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch-creating-rpms.html
