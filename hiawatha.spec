Summary:	An advanced and secure webserver for Unix
Name:		hiawatha
Version:	11.6
Release:	1
Source0:	https://hiawatha.leisink.net/files/hiawatha-11.6.tar.gz
Source1:	hiawatha.service
License:	GPLv2
Group:		System/Servers
Url:		http://hiawatha.leisink.net/
BuildRequires:	libxslt-devel
BuildRequires:	pkcs11-helper-devel
BuildRequires:	mbedtls-devel
BuildRequires:	cmake >= 2.8.4
BuildRequires:	ninja
Requires(preun):rpm-helper
Requires(post):	rpm-helper
Provides:	webserver

%description
Hiawatha is an advanced and secure webserver for Unix. It has been written 
with 'being secure' as its main goal. This resulted in a webserver which 
has for example DoS protection, connection control and traffic throttling. 
It has of course also thoroughly been checked and tested for buffer overflows

%prep
%autosetup -p1
# FIXME use system mbedtls once hiawatha starts
# supporting current versions
%cmake \
	-DENABLE_CHROOT:BOOL=ON \
	-DENABLE_MONITOR:BOOL=ON \
	-DUSE_PKCS11_HELPER_LIBRARY:BOOL=ON \
	-DCMAKE_SKIP_RPATH:BOOL=OFF \
	-DWEBROOT_DIR=/srv/www \
	-DPID_DIR=/run/hiawatha \
	-DUSE_SYSTEM_MBEDTLS:BOOL=OFF \
	-DUSE_STATIC_MBEDTLS_LIBRARY:BOOL=ON \
	-DINSTALL_MBEDTLS_HEADERS:BOOL=OFF \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

install -D -m 644 build/logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
#sed -i -e 's|/usr/var/log/hiawatha/|/var/log/hiawatha/|' %{buildroot}%{_sysconfdir}/%{name}/hiawatha.conf

install -D -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/hiawatha.service

rm -rf %{buildroot}%{_libdir}/hiawatha/libmbed*


%files
%dir /var/log/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_bindir}/lefh
%{_sbindir}/%{name}
%{_mandir}/*/*.*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/%{name}*
%{_bindir}/ssi-cgi
%{_sbindir}/cgi-wrapper
%{_sbindir}/wigwam
%{_libdir}/hiawatha
/srv/www
