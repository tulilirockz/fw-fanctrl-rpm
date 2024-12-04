%global jobid 899
%global debug_package %{nil}

%global reponame    fw-fanctrl
%global commit      f492140b48931518f30326131d97c79dacd9c462
%global commit_date 20241107
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .%{commit_date}.git%{shortcommit}

Name:           fw-fanctrl
Version:        0.0.0
Release:        1%{gitrel}%{?dist}
Summary:        Framework FanControl Software

License:        BSD-3-Clause
URL:            https://github.com/TamtamHero/fw-fanctrl
Source0:        https://github.com/TamtamHero/fw-fanctrl/archive/%{commit}/%{reponame}-%{shortcommit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  unzip
Requires:       python3
Requires:       libftdi
Requires:       framework-ec

%description
Framework Fan control script

%prep
%autosetup -n %{name}-%{commit}

%install
mkdir -p %{buildroot}%{_libdir}/systemd/system \
	%{buildroot}%{_bindir} \
	%{buildroot}%{_sysconfdir}/%{name}

chmod +x fanctrl.py
cp fanctrl.py %{buildroot}%{_bindir}
cp config.json %{buildroot}%{_sysconfdir}/%{name}
sed -i "s/%PREFIX_DIRECTORY%/\/usr/g" services/fw-fanctrl.service
sed -i "s/%NO_BATTERY_SENSOR_OPTION%//g" services/fw-fanctrl.service
sed -i "s/%SYSCONF_DIRECTORY%/\/etc/g" services/fw-fanctrl.service
cp services/fw-fanctrl.service %{buildroot}%{_libdir}/systemd/system

%post
%systemd_post fw-fanctrl.service

%preun
%systemd_preun fw-fanctrl.service

%postun
%systemd_postun fw-fanctrl.service

%files
%license LICENSE
%{_libdir}/systemd/system/%{name}.service
%{_sysconfdir}/%{name}/config.json
%attr(0755,root,root) %{_bindir}/fanctrl.py

%changelog
%autochangelog
