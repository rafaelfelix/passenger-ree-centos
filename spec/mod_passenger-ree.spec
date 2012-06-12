%global debug_package %{nil}
%define ree_prefix /opt/ruby
%define apache_module_path /etc/httpd/modules
%define passenger_root %{ree_prefix}/lib/ruby/gems/1.8/gems/passenger-%{version}
%define passenger_ext_apache2 %{passenger_root}/ext/apache2

Summary: Apache Module for Phusion Passenger built against Ruby Enterprise Edition
Name: mod_passenger-ree
Version: 3.0.12
Release: 1%{?dist}
Packager: Rafael Felix Correa <rafael.felix@rf4solucoes.com.br>
License: Modified BSD
Group: System Environment/Daemons
URL: http://www.modrails.com/
Requires: libselinux httpd apr apr-util ruby-enterprise ruby-enterprise-rubygems

BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
BuildRequires: ruby-enterprise ruby-enterprise-rubygems httpd-devel curl-devel zlib-devel

Source: passenger-%{version}.tar.gz

%description
Phusion Passenger™ — a.k.a. mod_rails or mod_rack — makes deployment
of Ruby web applications, such as those built on the revolutionary
Ruby on Rails web framework, a breeze. It follows the usual Ruby on
Rails conventions, such as “Don’t-Repeat-Yourself”.

This package contains the pluggable Apache server module for Passenger, built against Ruby Enterprise Edition

%prep
%setup -c -n %{name}-%{version}

%build
$RPM_BUILD_DIR/%{name}-%{version}/bin/passenger-install-apache2-module -a --apxs2-path=/usr/sbin/apxs

%install
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/phusion-passenger
mkdir -p ${RPM_BUILD_ROOT}%{passenger_root}/ext
cp -a $RPM_BUILD_DIR/%{name}-%{version}/agents ${RPM_BUILD_ROOT}/usr/lib/phusion-passenger
cp -a $RPM_BUILD_DIR/%{name}-%{version}/ext/apache2 ${RPM_BUILD_ROOT}%{passenger_root}/ext

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%exclude %{passenger_ext_apache2}/*.h
%exclude %{passenger_ext_apache2}/*.c
%exclude %{passenger_ext_apache2}/*.cpp
%exclude %{passenger_ext_apache2}/*.hpp
%exclude %{passenger_ext_apache2}/module_libboost_oxt/*.cpp
%exclude %{passenger_ext_apache2}/module_libpassenger_common/*.cpp
%{passenger_ext_apache2}/
/usr/lib/phusion-passenger/
%doc DEVELOPERS.TXT
%doc INSTALL
%doc LICENSE
%doc NEWS
%doc PACKAGING.TXT
%doc README
%doc doc/

%post
rm -f %{apache_module_path}/mod_passenger.so
ln -s %{passenger_ext_apache2}/mod_passenger.so %{apache_module_path}/mod_passenger.so

cat > /etc/httpd/conf.d/passenger.conf << EOF
## load
LoadModule    passenger_module     modules/mod_passenger.so

## setup
PassengerRoot %{passenger_root}
PassengerRuby /opt/ruby/bin/ruby
EOF

## APACHE RESTART
/etc/init.d/httpd restart

%postun
rm -f %{apache_module_path}/mod_passenger.so
rm -f /etc/httpd/conf.d/passenger.conf

## APACHE RESTART
/etc/init.d/httpd restart

%changelog
* Sun Jun 12 2012 Rafael Felix Correa <rafael.felix@rf4solucoes.com.br>
- brought agents/ to the package, under /usr/lib/phusion-passenger
- brought ext/apache2 to the package, excluding the source files
- added a post script to symlink the passenger_root/ext/apache2/mod_passenger.so inside /etc/httpd/modules

* Sun Jun 11 2012 Rafael Felix Correa <rafael.felix@rf4solucoes.com.br>
- updated the package requirements list
- added a post script to update the httpd configuration and restart it after installation

* Sun Jun 10 2012 Rafael Felix Correa <rafael.felix@rf4solucoes.com.br>
- first build of passenger-ree package
