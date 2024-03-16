%bcond_with autogen

Name:           mkp224o
Version:        1.7.0
Release:        1%{?dist}
Summary:        Vanity address generator for tor onion v3 (ed25519) hidden services

License:        CC0-1.0
URL:            https://github.com/cathugger/mkp224o
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}-src.tar.gz
Source1:        %{url}/releases/download/v%{version}/%{name}-%{version}-src.tar.gz.sig
# dnf install distribution-gpg-keys-1.102
# gpg2 --import --import-options import-export,import-minimal /usr/share/distribution-gpg-keys/mkp224o/cathugger.asc > ./mkp224o.keyring
Source2:        mkp224o.keyring

%if %{with autogen}
BuildRequires:  autoconf
%endif
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  gnupg2
BuildRequires:  make
BuildRequires:  pkgconfig(libsodium)

%description
This tool generates vanity ed25519 (hidden service version 3, formerly known as
proposal 224) onion addresses.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup

%build
# autogen.sh will generate a configure script if missing
%if %{with autogen}
./autogen.sh
%endif
CFLAGS='%{build_cflags} -Wa,--noexecstack'
CXXFLAGS='%{build_cxxflags} -Wa,--noexecstack'
LDFLAGS='%{build_ldflags} -Wl,-z,noexecstack'
# Reference: OPTIMIZATION.txt
%ifarch %{x86_64}
%configure --enable-amd64-51-30k
%else
%configure --enable-donna
%endif
%make_build

%install
install -Dm 755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license COPYING.txt
%doc OPTIMISATION.txt README.md
%{_bindir}/%{name}

%changelog
* Sat Mar 16 2024 Release <siliconwaffle@trilbyproject.org> - 1.7.0-1
- Initial RPM Release
