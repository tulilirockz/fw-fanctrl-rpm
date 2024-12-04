%global jobid 899
%global debug_package %{nil}

%global reponame    fw-fanctrl
%global commit      f492140b48931518f30326131d97c79dacd9c462
%global commit_date 20241107
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .%{commit_date}.git%{shortcommit}

Name:           fw-fanctrl
Version:        0.0.0
Release:        4%{gitrel}%{?dist}
Summary:        Framework FanControl Software

License:        BSD-3-Clause
URL:            https://github.com/TamtamHero/fw-fanctrl
Source0:        https://github.com/TamtamHero/fw-fanctrl/archive/%{commit}/%{reponame}-%{shortcommit}.tar.gz

BuildRequires:  systemd-rpm-macros
Requires:       python3
Requires:       fw-ectool

%description
Framework Fan control script

%prep
%autosetup -n %{name}-%{commit}

%build
chmod +x fanctrl.py
sed -i "s/%PREFIX_DIRECTORY%/\/usr/g" services/fw-fanctrl.service
sed -i "s/%PREFIX_DIRECTORY%/\/usr/g" services/system-sleep/fw-fanctrl-suspend
sed -i "s/%NO_BATTERY_SENSOR_OPTION%//g" services/fw-fanctrl.service
sed -i "s/%SYSCONF_DIRECTORY%/\/etc/g" services/fw-fanctrl.service

%install
install -Dm755 fanctrl.py %{buildroot}%{_bindir}/fanctrl.py
install -Dm644 services/system-sleep/%{name}-suspend %{buildroot}%{_libdir}/systemd/system-sleep/%{name}-suspend
install -Dm644 services/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -Dm755 config.json %{buildroot}%{_sysconfdir}/%{name}/config.json


%post
%systemd_post fw-fanctrl.service

%preun
%systemd_preun fw-fanctrl.service

%postun
%systemd_postun fw-fanctrl.service

%files
%license LICENSE
%{_unitdir}/%{name}.service
%{_sysconfdir}/%{name}/config.json
%{_libdir}/systemd/system-sleep/%{name}-suspend
%attr(0755,root,root) %{_bindir}/fanctrl.py

%changelog
%autochangelog
