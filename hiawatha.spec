Summary:	An advanced and secure webserver for Unix
Name:		hiawatha
Version:	9.4
Release:	3
Source0:	http://www.hiawatha-webserver.org/files/%{name}-%{version}.tar.gz
Source1:	hiawatha.service
License:	GPLv2
Group:		System/Servers
Url:		http://www.hiawatha-webserver.org/
BuildRequires:	libxslt-devel
BuildRequires:	pkcs11-helper-devel
BuildRequires:	polarssl-devel
BuildRequires:	cmake >= 2.8.4
Requires(preun):rpm-helper
Requires(post):	rpm-helper
Provides:	webserver


%description
Hiawatha is an advanced and secure webserver for Unix. It has been written 
with 'being secure' as its main goal. This resulted in a webserver which 
has for example DoS protection, connection control and traffic throttling. 
It has of course also thoroughly been checked and tested for buffer overflows

%prep
%setup -q
rm -rf polarssl

%build
%cmake	-DENABLE_CHROOT:BOOL=ON \
	-DENABLE_MONITOR:BOOL=ON \
	-DUSE_PKCS11_HELPER_LIBRARY:BOOL=ON \
	-DUSE_SYSTEM_POLARSSL:BOOL=ON \
	-DCMAKE_SKIP_RPATH:BOOL=OFF \
	-DCMAKE_INSTALL_LOCALSTATEDIR:PATH=var \
	-DCMAKE_INSTALL_PREFIX:PATH="" \
	-DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
	-DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
	-DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
	-DCMAKE_INSTALL_MANDIR:PATH=%{_mandir}
%make

%install
pushd build
%makeinstall_std

install -D -m 644 logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
perl -pi -e 's|/usr/var/log/hiawatha/|/var/log/hiawatha/|' %{buildroot}%{_sysconfdir}/%{name}/hiawatha.conf

install -D -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/hiawatha.service
popd

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%dir /var/log/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_sbindir}/%{name}
%{_mandir}/*/*.*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_localstatedir}/www/%{name}/
%{_unitdir}/%{name}*
%{_bindir}/ssi-cgi
%{_sbindir}/cgi-wrapper
%{_sbindir}/wigwam
