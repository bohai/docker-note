Name:fleet
Version:    0.1
Release:        1
Summary: Fleet - a distributed init system

Group:  Application
License:GPL
URL:    https://github.com/litevirt/fleet
Source0:fleet-0.1.tar.gz


%description
Fleet - a distributed init system

%prep
%setup -q

%build
./build

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 755 bin/fleetctl $RPM_BUILD_ROOT/usr/bin/fleetctl
install -m 755 bin/fleetd $RPM_BUILD_ROOT/usr/bin/fleetd
mkdir -p $RPM_BUILD_ROOT/etc/fleet
install -m 644 fleet.conf.sample $RPM_BUILD_ROOT/etc/fleet/fleet.conf

%files
/usr/bin/fleetd
/usr/bin/fleetctl
/etc/fleet/fleet.conf


%changelog
