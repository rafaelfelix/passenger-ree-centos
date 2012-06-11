%global debug_package %{nil}
%define ree_prefix /opt/ruby
%define apache_module_path /etc/httpd/modules

Summary: Apache Module for Phusion Passenger built against Ruby Enterprise Edition
Name: mod_passenger-ree
Version: 3.0.12
Release: 1%{?OSshort}
Packager: Rafael Felix Correa <rafael.felix@rf4solucoes.com.br>
License: Modified BSD
Group: System Environment/Daemons
URL: http://www.modrails.com/
Requires: libselinux
Requires: httpd

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
cd $RPM_BUILD_DIR/%{name}-%{version}
env APXS2=/usr/sbin/apxs %{ree_prefix}/bin/rake apache2 APACHE2_OUTPUT_DIR=${RPM_BUILD_ROOT}%{apache_module_path}

%install
# no-op

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/etc/httpd/modules/mod_passenger.so
%exclude %{apache_module_path}/*.o
%exclude %{apache_module_path}/*.a
%exclude %{apache_module_path}/module_libpassenger_common
%exclude %{apache_module_path}/module_libboost_oxt
%doc DEVELOPERS.TXT
%doc INSTALL
%doc LICENSE
%doc NEWS
%doc PACKAGING.TXT
%doc README
%doc doc/

%changelog
* Sun Jun 10 2012 Rafael Felix Correa <rafael.felix@rf4solucoes.com.br>
- first build of passenger-ree package
