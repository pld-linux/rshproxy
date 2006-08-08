Summary:	rshproxy is an application level gateway for the remote shell protocol
Summary(pl):	rshproxy jest aplikacyjn± bramk± dla protoko³u remote shell
Name:		rshproxy
Version:	1.0.3
Release:	3
License:	GPL
Group:		Applications/Networking
Source0:	http://www.quietsche-entchen.de/download/%{name}-%{version}.tar.gz
# Source0-md5:	eb147a7adf67185e3e7098f62ad1ddd0
Source1:	%{name}.inetd
Patch0:		%{name}-crypt.patch
URL:		http://www.quietsche-entchen.de/software/rsh.proxy.html
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	rc-inetd >= 0.8.1
Conflicts:	proxytools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rsh.proxy is a proxy server for remote shell protocol.

%description -l pl
rsh.proxy jest aplikacyjn± bramk± dla protoko³u zdalnego shella
(remote shell).

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1,/etc/sysconfig/rc-inetd}

install rsh.proxy $RPM_BUILD_ROOT%{_sbindir}
install rsh.proxy.1 $RPM_BUILD_ROOT%{_mandir}/man1

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/rshproxy


%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd reload

%postun
if [ "$1" = "0" ]; then
	%service -q rc-inetd  reload
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/rshproxy
%attr(755,root,root) %{_sbindir}/rsh.proxy
%{_mandir}/man1/*
