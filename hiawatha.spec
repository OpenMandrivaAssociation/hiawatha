%define name hiawatha
%define version 4.3.2
%define release %mkrel 3

Summary: Hiawatha, an advanced and secure webserver for Unix
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Source1: %{name}-sysvscript.bz2
License: GPL
Group: Networking/WWW
Url: http://projects.leisink.org/index.php?page=hiawatha
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: openssl-devel
Requires(pre): rpm-helper
Requires(post): rpm-helper
Provides: http-server


%description
Hiawatha is an advanced and secure webserver for Unix. It has been written 
with 'being secure' as its main goal. This resulted in a webserver which 
has for example DoS protection, connection control and traffic throttling. 
It has of course also thoroughly been checked and tested for buffer overflows

%prep
%setup -q

%build
%configure --enable-command --enable-ssl --enable-plugin
%make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/log/hiawatha
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/
install -m 644 etc/logrotate.d/%name $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%name
mkdir -p $RPM_BUILD_ROOT/var/log/%name
perl -pi -e 's|/var/lib/log/|/var/log/|' $RPM_BUILD_ROOT%{_sysconfdir}/%name/*

bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_initrddir}/%{name}

%post
%_post_service hiawatha

%preun
%_preun_service hiawatha

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(6711,root,root) %{_sbindir}/cgi_wrapper

%dir %{_sysconfdir}/%{name}
%dir /var/log/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_sbindir}/%{name}
%{_mandir}/*/*.*
%config(noreplace) %{_sysconfdir}/logrotate.d/%name
%{_localstatedir}/lib/www/%name.html
%attr(0755,root,root) %{_initrddir}/%name

